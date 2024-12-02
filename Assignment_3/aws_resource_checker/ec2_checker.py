import boto3
from utils import log_message, save_report
from compliance_rules import fetch_compliance_rules

def check_ec2_compliance():
    """
    Checks EC2 instance compliance against dynamically fetched rules.
    """
    log_message("Fetching EC2 compliance rules...")
    compliance_rules = fetch_compliance_rules("ec2")

    if not compliance_rules:
        log_message("No compliance rules available for EC2. Skipping compliance checks.", level="ERROR")
        return

    log_message("Starting EC2 compliance check...")
    ec2 = boto3.client("ec2")
    try:
        response = ec2.describe_instances()
    except Exception as e:
        log_message(f"Failed to describe EC2 instances: {e}", level="ERROR")
        return

    instances = response.get("Reservations", [])
    log_message(f"Found {len(instances)} EC2 instances.")

    non_compliant_instances = []

    for reservation in instances:
        for instance in reservation.get("Instances", []):
            instance_id = instance["InstanceId"]
            log_message(f"Checking compliance for EC2 instance: {instance_id}")

            instance_issues = []

            # 1. Check for the use of recommended AMIs
            ami_id = instance.get("ImageId", "")
            if ami_id != "ami-xxxxxxxxxxxxxxxxx":  # Replace with actual recommended AMI ID
                instance_issues.append(f"Instance {instance_id} is not using the recommended AMI.")

            # 2. Check Security Groups (Ensure no unrestricted access)
            for security_group in instance.get("SecurityGroups", []):
                sg_id = security_group["GroupId"]
                try:
                    sg_response = ec2.describe_security_groups(GroupIds=[sg_id])
                    for sg in sg_response.get("SecurityGroups", []):
                        for ip_permission in sg.get("IpPermissions", []):
                            if "0.0.0.0/0" in [ip_range.get("CidrIp") for ip_range in ip_permission.get("IpRanges", [])]:
                                instance_issues.append(f"Instance {instance_id} has unrestricted access in security group {sg_id}.")
                except Exception as e:
                    log_message(f"Failed to check security group {sg_id} for instance {instance_id}: {e}", level="ERROR")

            # 3. Verify EC2 Key Pair
            key_name = instance.get("KeyName", "")
            if not key_name:
                instance_issues.append(f"Instance {instance_id} does not have an associated key pair.")

            # 4. Ensure Instances Are Properly Tagged
            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
            if "Name" not in tags:
                instance_issues.append(f"Instance {instance_id} is not properly tagged with 'Name'.")

            # Add issues to the list if any
            if instance_issues:
                non_compliant_instances.append({
                    "InstanceId": instance_id,
                    "Issues": instance_issues
                })

    # Save the compliance report
    if non_compliant_instances:
        save_report(non_compliant_instances, "reports/ec2_compliance_report.json")
    else:
        log_message("All EC2 instances are compliant!")


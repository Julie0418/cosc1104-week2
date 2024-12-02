import boto3
from utils import log_message, save_report
from compliance_rules import fetch_compliance_rules

def check_ec2_compliance():
    """
    Checks EC2 instance compliance against dynamically fetched rules.
    """
    log_message("Fetching EC2 compliance rules...")
    compliance_rules = fetch_compliance_rules("ec2")

    log_message("Starting EC2 compliance check...")
    ec2 = boto3.client("ec2")
    try:
        response = ec2.describe_instances()
    except Exception as e:
        log_message(f"Failed to describe EC2 instances: {e}", level="ERROR")
        return

    non_compliant_instances = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance["InstanceId"]
            log_message(f"Checking compliance for instance: {instance_id}")

            # Example: Security group check
            for sg in instance.get("SecurityGroups", []):
                if sg["GroupName"] == "default":
                    non_compliant_instances.append({
                        "InstanceId": instance_id,
                        "Issue": "Using default security group"
                    })

    save_report(non_compliant_instances, "reports/ec2_compliance_report.json")

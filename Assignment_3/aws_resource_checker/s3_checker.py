import boto3
from utils import log_message, save_report
from compliance_rules import fetch_compliance_rules

def check_s3_compliance():
    """
    Checks S3 bucket compliance against dynamically fetched rules.
    """
    log_message("Fetching S3 compliance rules...")
    compliance_rules = fetch_compliance_rules("s3")

    if not compliance_rules:
        log_message("No compliance rules available for S3. Skipping compliance checks.", level="ERROR")
        return

    log_message("Starting S3 compliance check...")
    s3 = boto3.client("s3")
    try:
        response = s3.list_buckets()
    except Exception as e:
        log_message(f"Failed to list S3 buckets: {e}", level="ERROR")
        return

    buckets = response.get("Buckets", [])
    log_message(f"Found {len(buckets)} S3 buckets.")

    non_compliant_buckets = []

    for bucket in buckets:
        bucket_name = bucket["Name"]
        log_message(f"Checking compliance for bucket: {bucket_name}")

        bucket_issues = []

        # 1. Block Public Access Check
        try:
            block_public_access = s3.get_public_access_block(Bucket=bucket_name)
            block_all_public_access = block_public_access.get('PublicAccessBlockConfiguration', {}).get('BlockPublicAcls', False)
            if not block_all_public_access:
                bucket_issues.append("Block public access is not enabled for this bucket.")
        except s3.exceptions.ClientError as e:
            log_message(f"Failed to check Block Public Access settings for bucket {bucket_name}: {e}", level="ERROR")
            bucket_issues.append("Failed to verify Block Public Access settings.")

        # 2. Encryption Check
        try:
            encryption = s3.get_bucket_encryption(Bucket=bucket_name)
            if "ServerSideEncryptionConfiguration" not in encryption:
                bucket_issues.append("Bucket does not have encryption enabled")
        except s3.exceptions.ClientError as e:
            if "ServerSideEncryptionConfigurationNotFoundError" in str(e):
                bucket_issues.append("Bucket does not have encryption enabled")
            else:
                log_message(f"Failed to check encryption for bucket {bucket_name}: {e}", level="ERROR")

        # 3. Versioning Check
        try:
            versioning = s3.get_bucket_versioning(Bucket=bucket_name)
            if versioning.get("Status") != "Enabled":
                bucket_issues.append("Bucket versioning is not enabled")
        except s3.exceptions.ClientError as e:
            log_message(f"Failed to check versioning for bucket {bucket_name}: {e}", level="ERROR")
            bucket_issues.append("Failed to verify versioning settings.")

        # 4. Logging Check (Ensure access logging is enabled)
        try:
            logging = s3.get_bucket_logging(Bucket=bucket_name)
            if "LoggingEnabled" not in logging:
                bucket_issues.append("Bucket logging is not enabled")
        except s3.exceptions.ClientError as e:
            log_message(f"Failed to check logging for bucket {bucket_name}: {e}", level="ERROR")
            bucket_issues.append("Failed to verify logging settings.")

        # 5. MFA Delete Check (Ensure MFA delete is enabled)
        try:
            versioning = s3.get_bucket_versioning(Bucket=bucket_name)
            if versioning.get("MFADelete") != "Enabled":
                bucket_issues.append("MFA Delete is not enabled")
        except s3.exceptions.ClientError as e:
            log_message(f"Failed to check MFA Delete for bucket {bucket_name}: {e}", level="ERROR")
            bucket_issues.append("Failed to verify MFA Delete setting.")

        # 6. Cross-account Access Check (Only check if policy exists)
        try:
            try:
                policy = s3.get_bucket_policy(Bucket=bucket_name)
                if "Statement" in policy:
                    for statement in policy["Statement"]:
                        if "Principal" in statement and "*" in statement["Principal"]:
                            bucket_issues.append("Bucket allows cross-account access")
            except s3.exceptions.ClientError as e:
                if "NoSuchBucketPolicy" in str(e):
                    log_message(f"No bucket policy found for bucket {bucket_name}, skipping cross-account access check.", level="INFO")
                else:
                    raise e
        except s3.exceptions.ClientError as e:
            log_message(f"Failed to check cross-account access for bucket {bucket_name}: {e}", level="ERROR")
            bucket_issues.append("Failed to verify cross-account access settings.")

        # Add issues to the list if any
        if bucket_issues:
            non_compliant_buckets.append({
                "BucketName": bucket_name,
                "Issues": bucket_issues
            })

    # Save the compliance report
    if non_compliant_buckets:
        save_report(non_compliant_buckets, "reports/s3_compliance_report.json")
    else:
        log_message("All buckets are compliant!")

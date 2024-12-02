import boto3
from utils import log_message, save_report
from compliance_rules import fetch_compliance_rules

def check_s3_compliance():
    """
    Checks S3 bucket compliance against dynamically fetched rules.
    """
    log_message("Fetching S3 compliance rules...")
    compliance_rules = fetch_compliance_rules("s3")

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

        # Example: Public access block check
        try:
            public_access = s3.get_bucket_policy_status(Bucket=bucket_name)
            is_public = public_access.get("PolicyStatus", {}).get("IsPublic", False)
            if is_public:
                non_compliant_buckets.append({
                    "BucketName": bucket_name,
                    "Issue": "Bucket is publicly accessible"
                })
        except Exception as e:
            log_message(f"Failed to check public access for bucket {bucket_name}: {e}", level="ERROR")

    save_report(non_compliant_buckets, "reports/s3_compliance_report.json")

import argparse
from ec2_checker import check_ec2_compliance
from s3_checker import check_s3_compliance
from utils import log_message

def main():
    parser = argparse.ArgumentParser(description="AWS Resource Compliance Checker")
    parser.add_argument(
        "--service",
        choices=["ec2", "s3"],
        required=True,
        help="Select the AWS service to check compliance for (ec2 or s3)"
    )
    args = parser.parse_args()

    log_message("Starting compliance checks...")
    
    if args.service == "ec2":
        check_ec2_compliance()
    elif args.service == "s3":
        check_s3_compliance()
    else:
        log_message("Invalid service selected.", level="ERROR")

if __name__ == "__main__":
    main()

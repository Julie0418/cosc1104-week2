import boto3
import pandas as pd
import argparse
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to validate AWS resource response
def validate_aws_response(response, resource_name):
    if not response:
        logging.warning(f"No data returned for {resource_name}.")
        return False
    return True

# Function to get active EC2 instances with tags
def get_ec2_instances():
    logging.info("Fetching EC2 instance details...")
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_instances()
    except Exception as e:
        logging.error(f"Failed to describe EC2 instances: {e}")
        return pd.DataFrame()

    instances = []
    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            state = instance['State']['Name']
            if state == 'running':
                # Fetch tags for EC2 instance
                tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': state,
                    'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                    'Tags': tags,
                })
    logging.info(f"Found {len(instances)} running EC2 instances.")
    return pd.DataFrame(instances)

# Function to get active S3 buckets with storage usage
def get_s3_buckets():
    logging.info("Fetching S3 bucket details...")
    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
    except Exception as e:
        logging.error(f"Failed to list S3 buckets: {e}")
        return pd.DataFrame()

    buckets = []
    for bucket in response.get('Buckets', []):
        bucket_name = bucket['Name']
        creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')

        # Fetching S3 bucket usage statistics
        try:
            storage_response = s3.list_objects_v2(Bucket=bucket_name)
            total_objects = storage_response.get('KeyCount', 0)
            total_size = sum(obj['Size'] for obj in storage_response.get('Contents', []))
        except Exception as e:
            logging.error(f"Failed to retrieve storage info for S3 bucket {bucket_name}: {e}")
            total_objects = total_size = 0

        buckets.append({
            'BucketName': bucket_name,
            'CreationDate': creation_date,
            'TotalObjects': total_objects,
            'TotalSizeMB': total_size / (1024 * 1024),  # Convert bytes to MB
        })
    logging.info(f"Found {len(buckets)} S3 buckets.")
    return pd.DataFrame(buckets)

# Function to get active RDS instances with snapshot and backup info
def get_rds_instances():
    logging.info("Fetching RDS instance details...")
    rds = boto3.client('rds')
    try:
        response = rds.describe_db_instances()
    except Exception as e:
        logging.error(f"Failed to describe RDS instances: {e}")
        return pd.DataFrame()

    db_instances = []
    for db_instance in response.get('DBInstances', []):
        if db_instance['DBInstanceStatus'] == 'available':
            # Fetch RDS backups and snapshots
            try:
                snapshots = rds.describe_db_snapshots(DBInstanceIdentifier=db_instance['DBInstanceIdentifier'])
                backups = []
                
                # Check if DBClusterIdentifier exists before fetching cluster backups
                if 'DBClusterIdentifier' in db_instance and db_instance['DBClusterIdentifier']:
                    backups = rds.describe_db_cluster_snapshots(DBClusterIdentifier=db_instance['DBClusterIdentifier'])
            except Exception as e:
                logging.error(f"Failed to retrieve backups for RDS instance {db_instance['DBInstanceIdentifier']}: {e}")
                snapshots = backups = []

            db_instances.append({
                'DBInstanceIdentifier': db_instance['DBInstanceIdentifier'],
                'DBInstanceClass': db_instance['DBInstanceClass'],
                'Status': db_instance['DBInstanceStatus'],
                'Engine': db_instance['Engine'],
                'LaunchTime': db_instance['InstanceCreateTime'].strftime('%Y-%m-%d %H:%M:%S'),
                'SnapshotsCount': len(snapshots) if isinstance(snapshots, list) else 0,
                'BackupsCount': len(backups) if isinstance(backups, list) else 0,
            })
    logging.info(f"Found {len(db_instances)} available RDS instances.")
    return pd.DataFrame(db_instances)

# Function to analyze EC2 costs with instance size and usage duration
def analyze_ec2_costs(df):
    if df.empty:
        logging.warning("No EC2 data to analyze.")
        return df
    # Advanced cost estimation logic based on instance types and usage duration
    cost_per_instance = {'t2.micro': 0.01, 't2.medium': 0.03, 't2.large': 0.05}  # Cost per hour (example)
    df['EstimatedCost'] = df['InstanceType'].apply(lambda x: cost_per_instance.get(x, 0.02) * 24 * 30)  # Monthly cost
    df['EstimatedCost'] = df['EstimatedCost'].round(2)  # Round the cost to 2 decimal places
    logging.info("EC2 cost analysis completed.")
    return df

# Function to validate file path for output CSV
def validate_file_path(output_file):
    # Check if the directory exists, if not create it
    directory = os.path.dirname(output_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    return True

# Function to generate a CSV report with a detailed format
def generate_report(ec2_df, s3_df, rds_df, output_file):
    # Validate that at least one resource type is available
    if ec2_df.empty and s3_df.empty and rds_df.empty:
        logging.warning("No resources to report. Exiting.")
        return

    # Validate file path before writing
    if not validate_file_path(output_file):
        return

    # Initialize list to hold DataFrames for merging
    data_frames = []

    # Add EC2 data if available
    if not ec2_df.empty:
        ec2_df['ResourceType'] = 'EC2'
        data_frames.append(ec2_df[['ResourceType', 'InstanceId', 'InstanceType', 'State', 'LaunchTime', 'Tags', 'EstimatedCost']])

    # Add S3 data if available
    if not s3_df.empty:
        s3_df['ResourceType'] = 'S3'
        data_frames.append(s3_df[['ResourceType', 'BucketName', 'CreationDate', 'TotalObjects', 'TotalSizeMB']])

    # Add RDS data if available
    if not rds_df.empty:
        rds_df['ResourceType'] = 'RDS'
        data_frames.append(rds_df[['ResourceType', 'DBInstanceIdentifier', 'DBInstanceClass', 'Status', 'Engine', 'LaunchTime', 'SnapshotsCount', 'BackupsCount']])

    # Concatenate all available dataframes
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Rearranging and formatting the columns
    combined_df = combined_df.rename(columns={
        'InstanceId': 'ResourceId',
        'BucketName': 'ResourceName',
        'DBInstanceIdentifier': 'ResourceName',
        'InstanceType': 'ResourceTypeDetails',
        'DBInstanceClass': 'ResourceTypeDetails',
        'State': 'Status',
        'Engine': 'DatabaseEngine',
        'LaunchTime': 'StartTime',
        'EstimatedCost': 'EstimatedMonthlyCost',
        'CreationDate': 'StartTime',
        'TotalObjects': 'TotalObjectsInBucket',
        'TotalSizeMB': 'TotalBucketSizeMB',
        'SnapshotsCount': 'TotalSnapshots',
        'BackupsCount': 'TotalBackups',
        'Tags': 'InstanceTags',
    })

    # Fixing StartTime duplication by removing the extra StartTime column
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    # Handling empty or irrelevant fields in non-applicable resources
    combined_df['DatabaseEngine'] = combined_df['DatabaseEngine'].fillna('N/A')
    combined_df['TotalSnapshots'] = combined_df['TotalSnapshots'].fillna(0)
    combined_df['TotalBackups'] = combined_df['TotalBackups'].fillna(0)

    # Writing to CSV file
    combined_df.to_csv(output_file, index=False)
    logging.info(f"Report generated: {output_file}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Advanced AWS Cost Monitoring")
    # Set the default output file to a relative path in the current working directory
    parser.add_argument('--output', default='aws_report.csv', help="Path to the output CSV file")
    args = parser.parse_args()

    # Fetch EC2, S3, and RDS data
    ec2_df = get_ec2_instances()
    s3_df = get_s3_buckets()
    rds_df = get_rds_instances()

    # Analyze EC2 costs
    ec2_df = analyze_ec2_costs(ec2_df)

    # Generate the final report
    generate_report(ec2_df, s3_df, rds_df, args.output)

if __name__ == "__main__":
    main()

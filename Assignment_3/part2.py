import boto3
import pandas as pd
import argparse
import os

# Function to get active EC2 instances
def get_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']
            if state == 'running':
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': state,
                    'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                })
    if not instances:
        print("No running EC2 instances found.")
    return pd.DataFrame(instances)

# Function to get active S3 buckets
def get_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        buckets.append({
            'BucketName': bucket['Name'],
            'CreationDate': bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S'),
        })
    if not buckets:
        print("No S3 buckets found.")
    return pd.DataFrame(buckets)

# Function to get active RDS instances
def get_rds_instances():
    rds = boto3.client('rds')
    response = rds.describe_db_instances()
    db_instances = []
    for db_instance in response['DBInstances']:
        if db_instance['DBInstanceStatus'] == 'available':
            db_instances.append({
                'DBInstanceIdentifier': db_instance['DBInstanceIdentifier'],
                'DBInstanceClass': db_instance['DBInstanceClass'],
                'Status': db_instance['DBInstanceStatus'],
                'Engine': db_instance['Engine'],
                'LaunchTime': db_instance['InstanceCreateTime'].strftime('%Y-%m-%d %H:%M:%S'),
            })
    if not db_instances:
        print("No available RDS instances found.")
    return pd.DataFrame(db_instances)

# Function to analyze EC2 instance costs
def analyze_ec2_costs(df):
    if df.empty:
        return df
    # Simplified cost estimation logic (dummy values for demonstration)
    cost_per_instance = {'t2.micro': 0.01, 't2.large': 0.05}  # Cost per hour (example)
    df['EstimatedCost'] = df['InstanceType'].apply(lambda x: cost_per_instance.get(x, 0.02) * 24 * 30)  # Monthly cost
    df['EstimatedCost'] = df['EstimatedCost'].round(2)  # Round the cost to 2 decimal places
    return df

# Function to generate a CSV report with readable format
def generate_report(ec2_df, s3_df, rds_df, output_file):
    # Check if there are any resources to report
    if ec2_df.empty and s3_df.empty and rds_df.empty:
        print("No resources to report. Exiting.")
        return
    
    # Initialize list to hold DataFrames for merging
    data_frames = []

    # Add EC2 data if available
    if not ec2_df.empty:
        ec2_df['ResourceType'] = 'EC2'
        data_frames.append(ec2_df[['ResourceType', 'InstanceId', 'InstanceType', 'State', 'LaunchTime', 'EstimatedCost']])

    # Add S3 data if available
    if not s3_df.empty:
        s3_df['ResourceType'] = 'S3'
        data_frames.append(s3_df[['ResourceType', 'BucketName', 'CreationDate']])

    # Add RDS data if available
    if not rds_df.empty:
        rds_df['ResourceType'] = 'RDS'
        data_frames.append(rds_df[['ResourceType', 'DBInstanceIdentifier', 'DBInstanceClass', 'Status', 'Engine', 'LaunchTime']])

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
    })

    # Fixing StartTime duplication by removing the extra StartTime column
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    # Ensure output file can be written
    if os.access(output_file, os.W_OK):
        combined_df.to_csv(output_file, index=False)
        print(f"Report generated: {output_file}")
    else:
        print(f"Error: Unable to write to the file '{output_file}'. Please check permissions.")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automated AWS Cost Monitoring")
    parser.add_argument('--output', type=str, default='cost_report.csv', help='Output file for the cost report')
    args = parser.parse_args()

    print("Fetching EC2 instance details...")
    ec2_data = get_ec2_instances()

    print("Fetching S3 bucket details...")
    s3_data = get_s3_buckets()

    print("Fetching RDS instance details...")
    rds_data = get_rds_instances()

    print("Analyzing EC2 costs...")
    analyzed_ec2_data = analyze_ec2_costs(ec2_data)

    print("Generating report...")
    generate_report(analyzed_ec2_data, s3_data, rds_data, args.output)

if __name__ == "__main__":
    main()

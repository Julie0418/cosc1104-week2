'''
Author: Sarvesh More and Julekha Khatoon
Date: 2024-11-01
Description: 3 will be given a very large list of AWS EC2 instances and (probably) some incomplete code to load and/or parse through the file.
For this exercise, we are going to make a console-based application where a user can enter their minimum required CPU cores (and, optionally, a maximum) 
and their minimum required memory in GiB (and, optionally, a maximum),
and then display to the user a list of all AWS EC2 instance types that support their needs.
In this simulation, the user will request cloud resources and your program will determine if the requested resources are available
based on some limit that is defined.

'''

import json

# Load the JSON data from the file
with open('ec2_instance_types.json') as ec2:
    ec2_data = json.load(ec2)

# Get CPU and memory requirements from user
min_cpu = int(input("Enter the minimum number of CPU cores: "))
max_cpu = input("Enter the maximum number of CPU cores (or press Enter to skip): ")
min_memory = float(input("Enter the minimum memory in GiB: "))
max_memory = input("Enter the maximum memory in GiB (or press Enter to skip): ")

# Convert max values to None if not provided
max_cpu = int(max_cpu) if max_cpu else None
max_memory = float(max_memory) if max_memory else None

# Function to filter EC2 instances
def filter_instances(data, min_cpu, max_cpu, min_memory, max_memory):
    results = []
    for instance in data:
        # Extract and convert values for comparison
        cpu = int(instance['vcpu'].split()[0])  # Assuming 'vcpu' format is always like "2 vCPUs"
        memory = float(instance['memory'].split()[0])  # Assuming 'memory' format is always like "0.5 GiB"
        
        # Check if instance meets CPU and memory requirements
        if cpu >= min_cpu and (max_cpu is None or cpu <= max_cpu) and \
           memory >= min_memory and (max_memory is None or memory <= max_memory):
            results.append(instance)
    return results

# Filter and display results
filtered_instances = filter_instances(ec2_data, min_cpu, max_cpu, min_memory, max_memory)

# Nicely format the output
print("Matching EC2 Instances:")
for instance in filtered_instances:
    print(f"Name: {instance['name']}, CPU: {instance['vcpu']}, Memory: {instance['memory']}, Bandwidth: {instance['bandwidth']}, Availability: {instance['availability']}")
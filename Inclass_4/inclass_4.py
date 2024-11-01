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

def get_valid_cpu_requirements():
    # Prompt the user for minimum and maximum CPU cores.
    while True:
        try:
            min_cpu = int(input("Enter minimum CPU cores required: "))
            max_cpu_input = input("Enter maximum CPU cores required (press Enter to skip): ")
            max_cpu = int(max_cpu_input) if max_cpu_input else None
            return min_cpu, max_cpu
        except ValueError:
            print("Invalid input. Please enter valid integer values for CPU cores.")

def get_valid_memory_requirements():
    # Prompt the user for minimum and maximum memory in GiB.
    while True:
        try:
            min_memory = float(input("Enter minimum memory (GiB) required: "))
            max_memory_input = input("Enter maximum memory (GiB) required (press Enter to skip): ")
            max_memory = float(max_memory_input) if max_memory_input else None
            return min_memory, max_memory
        except ValueError:
            print("Invalid input. Please enter valid numeric values for memory.")

def load_ec2_instances(filename):
    # Load EC2 instance types from the specified JSON file.
    with open(filename, 'r') as file:
        return json.load(file)

def extract_vcpu_count(vcpu_string):
    # Extract and return the numeric vCPU count from the vCPU string.
    return int(vcpu_string.split()[0])

def extract_memory_value(memory_string):
    # Extract and return the numeric memory value from the memory string.
    return float(memory_string.split()[0])

def filter_instances(ec2_instances, min_cpu, max_cpu, min_memory, max_memory):
    # Filter EC2 instances based on user-defined CPU and memory requirements.
    filtered_instances = []
    
    for instance in ec2_instances:
        cpu_cores = extract_vcpu_count(instance['vcpu'])
        memory = extract_memory_value(instance['memory'])
        
        # Check if the instance meets the CPU and memory criteria
        cpu_criteria = cpu_cores >= min_cpu and (max_cpu is None or cpu_cores <= max_cpu)
        memory_criteria = memory >= min_memory and (max_memory is None or memory <= max_memory)
        
        if cpu_criteria and memory_criteria:
            filtered_instances.append(instance)
    
    return filtered_instances

def display_instances(instances):
    # Display the filtered EC2 instance types in a user-friendly format.
    if instances:
        print("\nMatching EC2 Instance Types:\n" + "-"*30)
        for instance in instances:
            print(f"Instance Name: {instance['name']}")
            print(f" - vCPUs: {extract_vcpu_count(instance['vcpu'])}")
            print(f" - Memory: {extract_memory_value(instance['memory'])} GiB")
            print(f" - Storage: {instance['storage']}")
            print(f" - Bandwidth: {instance['bandwidth']}")
            print(f" - Availability: {instance['availability']}")
            print("-" * 30)
    else:
        print("No EC2 instance types found matching your requirements.")

def main():
    # Main function to run the EC2 instance filtering application.
    # Step 1: Get CPU requirements
    min_cpu, max_cpu = get_valid_cpu_requirements()
    
    # Step 2: Get memory requirements
    min_memory, max_memory = get_valid_memory_requirements()
    
    # Step 3: Load EC2 instances from JSON file
    ec2_instances = load_ec2_instances('ec2_instance_types.json')
    
    # Step 4: Filter instances based on requirements
    filtered_instances = filter_instances(ec2_instances, min_cpu, max_cpu, min_memory, max_memory)
    
    # Step 5: Display the results
    display_instances(filtered_instances)

if __name__ == "__main__":
    main()

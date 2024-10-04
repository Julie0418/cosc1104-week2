"""
Author: Sarvesh More and Julekha Khatoon
Date: 2024-09-27
Description: We are going to create a simple Python script using the main ideas covered early in this course.
It will simulate a cloud resource provisioning system. 
In this simulation, the user will request cloud resources and your program will determine if the requested resources are available based on some limit that is defined.
"""

# Constants defining available resources
TOTAL_CPU_CORES = 16  # Total CPU cores available
TOTAL_MEMORY_GB = 128  # Total memory available in gigabytes

# User input for required resources
try:
    required_cpu_cores = int(input("Enter the number of required CPU cores (must be a multiple of 2): "))
    required_memory_gb = float(input("Enter the amount of required memory in GB (float): "))

    # Input validation for negative values
    if required_cpu_cores < 0 or required_memory_gb < 0:
        print("Error: Resource requests cannot be negative.")
    # Check if required_cpu_cores is a multiple of 2
    elif required_cpu_cores % 2 != 0:
        print("Error: The number of CPU cores must be a multiple of 2.")
    else:
        # Check resource availability
        if (required_cpu_cores <= TOTAL_CPU_CORES) and (required_memory_gb <= TOTAL_MEMORY_GB):
            print("Resources provisioned successfully.")
            # Calculate remaining resources
            remaining_cpu_cores = TOTAL_CPU_CORES - required_cpu_cores
            remaining_memory_gb = TOTAL_MEMORY_GB - required_memory_gb
        else:
            print("Resource request exceeds capacity. Provisioning failed.")
            # Remaining resources in case of failure
            remaining_cpu_cores = TOTAL_CPU_CORES
            remaining_memory_gb = TOTAL_MEMORY_GB

        # Display remaining resources
        print(f"Remaining CPU cores: {remaining_cpu_cores}")
        print(f"Remaining memory (GB): {remaining_memory_gb}")

except ValueError:
    print("Error: Please enter valid numeric values.")
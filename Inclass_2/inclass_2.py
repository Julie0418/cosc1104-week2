''' 
 Author:  Julekha Khatoon and Sarvesh More 
 Date: 2024-09-27
 Description: We are extending the main idea of our simulation from the previous part, still doing a mock resource allocation app.
              However, this time it will incorporate both loops and lists. 
              Instead of checking whether one resource allocation request is valid, it will do as many as the user wants.
'''

# Constants
TOTAL_CPU_CORES = 32  # Total number of CPU cores available
TOTAL_MEMORY_GB = 64  # Total amount of memory available in gigabytes (GB)

# Lists to track resources
allocated_resources = []  # List to store allocated resources
pending_requests = []      # List to store pending requests

# Variables to track used resources
used_cpu_cores = 0
used_memory_gb = 0

# Initialize request flag
request_more = 'yes'

# Main loop for handling user requests
while request_more == 'yes':
    # User input for resource requests
    username = input("Enter username: ")

    # Input for CPU cores
    required_cpu_cores = int(input("Enter the number of required CPU cores (positive integer, multiple of 2): "))
    if required_cpu_cores < 0 or required_cpu_cores % 2 != 0:
        print("Error: The number of CPU cores must be a positive integer and a multiple of 2.")
    else:
        # Input for memory
        required_memory_gb = float(input("Enter the amount of required memory in GB (positive number): "))
        if required_memory_gb < 0:
            print("Error: Memory must be a positive number.")
        else:
            # Check resource availability
            if (used_cpu_cores + required_cpu_cores <= TOTAL_CPU_CORES) and \
               (used_memory_gb + required_memory_gb <= TOTAL_MEMORY_GB):
                # Allocate resources
                allocated_resources.append([username, required_cpu_cores, required_memory_gb])
                used_cpu_cores += required_cpu_cores
                used_memory_gb += required_memory_gb
                print("Resources provisioned successfully.")
            else:
                # Add to pending requests
                pending_requests.append([username, required_cpu_cores, required_memory_gb])
                print("Resource request exceeds capacity. Provisioning failed.")

    # Ask if the user wants to make another request
    request_more = input("Do you want to make another request? (yes/no): ").strip().lower()

# Display allocated resources
print("\nAllocated Resources:")
print("Username\tCPU Cores\tMemory (GB)")
for resource in allocated_resources:
    print(f"{resource[0]:<16}{resource[1]:<12}{resource[2]}")

# Display pending requests
print("\nPending Requests:")
print("Username\tCPU Cores\tMemory (GB)")
for request in pending_requests:
    print(f"{request[0]:<16}{request[1]:<12}{request[2]}")
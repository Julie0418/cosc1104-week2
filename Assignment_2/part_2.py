import os

# Function to check for files with zero size in a specified directory
def check_zero_size_files(directory):
    """
    This function checks a given directory for files with zero size.
    
    Args:
    - directory (str): The path of the directory to scan for empty files.
    
    Returns:
    - List[str]: A list of filenames that have zero size.
    """
    zero_size_files = []  # List to store names of zero-sized files
    
    # Check if the provided path is a valid directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return []

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)  # Get the full file path
        
        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)  # Get file size in bytes
            
            # If the file size is zero, add it to the list
            if file_size == 0:
                zero_size_files.append(filename)
    
    return zero_size_files


# Main function to interact with the user and display the results
def main():
    """
    This function prompts the user to input a directory path and displays the zero-sized files.
    """
    # Prompt the user to input the directory path
    directory_path = input("Enter the directory path to check for zero-sized files: ").strip()
    
    # Call the function to check for zero-sized files
    zero_size_files = check_zero_size_files(directory_path)
    
    # Display the results
    if zero_size_files:
        print("\nZero-sized files found:")
        for file in zero_size_files:
            print(f"- {file}")
    else:
        print("\nNo zero-sized files found.")


# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()

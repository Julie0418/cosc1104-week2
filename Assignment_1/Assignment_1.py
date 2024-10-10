# Lists to store usernames and their corresponding storage spaces
usernames = []
available_storage = []

def create_user_account(username, storage_space):
    # Validation for unique username and positive storage space
    if not username or username in usernames:
        print("Invalid username. It must be unique and not blank.")
        return
    
    # Username validation: Must contain at least one alphabet character
    if username.isdigit():
        print("Username cannot be entirely numeric. It must include alphabetic characters.")
        return
    
    if storage_space <= 0:
        print("Storage space must be a positive number.")
        return
    
    # Adding the user details to the lists
    usernames.append(username)
    available_storage.append(storage_space)
    print(f"User account '{username}' created with {storage_space}MB of storage.")

def upload_file(username, filename, filesize):
    # Check if user exists and has enough space
    if username not in usernames:
        print("User not found.")
        return
    
    # Validate filesize: It must be greater than 0
    if filesize <= 0:
        print("Filesize must be greater than 0MB.")
        return
    
    # Get the index of the user in the lists
    index = usernames.index(username)

    # Check if the user has enough storage space
    if available_storage[index] >= filesize:
        available_storage[index] -= filesize
        print(f"File '{filename}' uploaded successfully for user '{username}'.")
        print(f"Remaining storage for '{username}': {available_storage[index]}MB")
    else:
        print("Not enough storage space to upload this file.")

def delete_user_account(username):
    # Check if the user exists
    if username not in usernames:
        print("User not found.")
        return
    
    index = usernames.index(username)
    usernames.pop(index)
    available_storage.pop(index)
    print(f"User account '{username}' deleted successfully.")

def display_accounts():
    print("\nCurrent User Accounts:")
    for i in range(len(usernames)):
        print(f"Username: {usernames[i]}, Available Storage: {available_storage[i]}MB")
    print()

def get_valid_integer(prompt):
    # Loop until a valid integer is entered
    valid_input = False
    while not valid_input:
        user_input = input(prompt)
        if user_input.isdigit():
            valid_input = True
            return int(user_input)
        else:
            print("Invalid input. Please enter a valid numeric value.")

def main():
    running = True  # Flag to control the loop

    while running:
        print("\nMenu:")
        print("1. Create User Account")
        print("2. Delete User Account")
        print("3. Upload File")
        print("4. Display All Accounts")
        print("5. Exit")

        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            username = input("Enter username: ")
            
            # Ensure username contains at least one alphabetic character and is not only numbers
            if any(char.isalpha() for char in username):
                storage_space = get_valid_integer("Enter available storage space (in MB): ")
                create_user_account(username, storage_space)
            else:
                print("Invalid username. Username must contain at least one alphabetic character.")
        
        elif choice == '2':
            username = input("Enter username to delete: ")
            delete_user_account(username)
        
        elif choice == '3':
            username = input("Enter username: ")
            # Use an if-else structure to control the flow
            if username in usernames:
                filename = input("Enter filename: ")
                filesize = get_valid_integer("Enter filesize (in MB): ")
                upload_file(username, filename, filesize)
            else:
                print("User not found. Returning to menu.")
        
        elif choice == '4':
            display_accounts()
        
        elif choice == '5':
            print("Exiting the program.")
            running = False  # Change flag to exit the loop
        
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

# conversions.py

def gibi_to_giga(gibibytes):
    """Converts Gibibytes to Gigabytes."""
    return gibibytes * (1_073_741_824 / 1_000_000_000)

def giga_to_gibi(gigabytes):
    """Converts Gigabytes to Gibibytes."""
    return gigabytes * (1_000_000_000 / 1_073_741_824)

if __name__ == "__main__":
    running = True  # Control the loop with this flag

    while running:
        print("\nChoose an option:")
        print("1. Convert Gibibytes to Gigabytes")
        print("2. Convert Gigabytes to Gibibytes")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '3':
            print("Exiting program.")
            running = False  # Set flag to False to stop the loop
        elif choice == '1':
            user_input = input("Enter the number of Gibibytes to convert (or type 'q' to return to the menu): ")
            
            if user_input.lower() == 'q':
                print("Returning to the main menu.")
            else:
                try:
                    gibibytes = float(user_input)
                    if gibibytes < 0:
                        print("Please enter a positive number.")
                    else:
                        gigabytes = gibi_to_giga(gibibytes)
                        print(f"{gibibytes} GiB is equal to {gigabytes:.4f} GB.")
                except ValueError:
                    print("Invalid input. Please enter a valid number or 'q' to return to the menu.")
        elif choice == '2':
            user_input = input("Enter the number of Gigabytes to convert (or type 'q' to return to the menu): ")

            if user_input.lower() == 'q':
                print("Returning to the main menu.")
            else:
                try:
                    gigabytes = float(user_input)
                    if gigabytes < 0:
                        print("Please enter a positive number.")
                    else:
                        gibibytes = giga_to_gibi(gigabytes)
                        print(f"{gigabytes} GB is equal to {gibibytes:.4f} GiB.")
                except ValueError:
                    print("Invalid input. Please enter a valid number or 'q' to return to the menu.")
        else:
            print("Invalid choice, please select 1, 2, or 3.")

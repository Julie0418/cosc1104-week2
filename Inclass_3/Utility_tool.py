def is_positive(number):
    """Checks if a number is positive."""
    return number > 0

def gibi_to_giga(gibibytes):
    """Converts Gibibytes to Gigabytes."""
    return gibibytes * (1_073_741_824 / 1_000_000_000)

def giga_to_gibi(gigabytes):
    """Converts Gigabytes to Gibibytes."""
    return gigabytes * (1_000_000_000 / 1_073_741_824)

def sum_of_digits(number):
    """Returns the sum of the digits of a positive integer."""
    return sum(int(digit) for digit in str(number))

def main():
    running = True  # Control the loop with this flag

    while running:
        print("\nChoose an option:")
        print("1. Check if a number is positive")
        print("2. Convert Gibibytes to Gigabytes")
        print("3. Convert Gigabytes to Gibibytes")
        print("4. Find the sum of the digits of a positive integer")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting program.")
            running = False  # Set flag to False to stop the loop
        elif choice == '1':
            user_input = input("Enter a number to check if it is positive (or type 'q' to return to the menu): ")
            if user_input.lower() == 'q':
                print("Returning to the main menu.")
            else:
                try:
                    number = float(user_input)
                    result = is_positive(number)
                    print(f"The number {number} is positive: {result}")
                except ValueError:
                    print("Invalid input. Please enter a valid number or 'q' to return to the menu.")
        
        elif choice == '2':
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

        elif choice == '3':
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

        elif choice == '4':
            user_input = input("Enter a positive integer to find the sum of its digits (or type 'q' to return to the menu): ")
            if user_input.lower() == 'q':
                print("Returning to the main menu.")
            else:
                try:
                    number = int(user_input)
                    if number < 0:
                        print("Please enter a positive integer.")
                    else:
                        result = sum_of_digits(number)
                        print(f"The sum of digits of {number} is {result}.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer or 'q' to return to the menu.")
        
        else:
            print("Invalid choice, please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()

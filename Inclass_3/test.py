# main.py

def is_positive(number):
    """Returns True if the number is positive, otherwise False."""
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

def get_positive_float(prompt):
    """Prompts the user for a positive float until a valid input is received."""
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'q':
            return None
        try:
            value = float(user_input)
            if value < 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number or 'q' to quit.")

def get_positive_integer(prompt):
    """Prompts the user for a positive integer until a valid input is received."""
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'q':
            return None
        try:
            value = int(user_input)
            if value < 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer or 'q' to quit.")

if __name__ == "__main__":
    running = True  # Control the loop with this flag

    while running:
        print("\nChoose an option:")
        print("1. Check if a number is positive")
        print("2. Convert Gibibytes to Gigabytes")
        print("3. Convert Gigabytes to Gibibytes")
        print("4. Find the sum of digits of a positive integer")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting program.")
            running = False  # Exit the loop
        elif choice == '1':
            user_input = input("Enter a number to check if it is positive (or type 'q' to return to the menu): ")
            
            if user_input.lower() == 'q':
                print("Exiting program.")
                running = False  # Exit the loop
            else:
                try:
                    number = float(user_input)
                    result = is_positive(number)
                    print(f"The number {number} is positive: {result}")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        elif choice == '2':
            gibibytes = get_positive_float("Enter the number of Gibibytes to convert (or type 'q' to quit): ")
            if gibibytes is None:
                print("Exiting program.")
                running = False
            else:
                gigabytes = gibi_to_giga(gibibytes)
                print(f"{gibibytes} GiB is equal to {gigabytes:.4f} GB.")
        elif choice == '3':
            gigabytes = get_positive_float("Enter the number of Gigabytes to convert (or type 'q' to quit): ")
            if gigabytes is None:
                print("Exiting program.")
                running = False
            else:
                gibibytes = giga_to_gibi(gigabytes)
                print(f"{gigabytes} GB is equal to {gibibytes:.4f} GiB.")
        elif choice == '4':
            number = get_positive_integer("Enter a positive integer to find the sum of its digits (or type 'q' to quit): ")
            if number is None:
                print("Exiting program.")
                running = False
            else:
                result = sum_of_digits(number)
                print(f"The sum of digits of {number} is {result}.")
        else:
            print("Invalid choice, please select 1, 2, 3, 4, or 5.")

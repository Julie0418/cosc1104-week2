# sum_of_digits.py

def sum_of_digits(number):
    """Returns the sum of the digits of a positive integer."""
    return sum(int(digit) for digit in str(number))

if __name__ == "__main__":
    running = True  # Control the loop with this flag

    while running:
        user_input = input("Enter a positive integer to find the sum of its digits (or type 'q' to quit): ")
        
        if user_input.lower() == 'q':
            print("Exiting program.")
            running = False  # Exit the loop
        else:
            try:
                number = int(user_input)
                if number < 0:
                    print("Please enter a positive integer.")
                else:
                    result = sum_of_digits(number)
                    print(f"The sum of digits of {number} is {result}.")
            except ValueError:
                print("Invalid input. Please enter a valid integer or 'q' to quit.")

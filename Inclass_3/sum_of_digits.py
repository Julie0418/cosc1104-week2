"""
Author: Sarvesh More and Julekha Khatoon
Date: 2024-10-4
Description: This script defines a function to calculate the sum of the digits of a 
positive integer. It prompts the user for input and allows them to compute the 
sum of digits for multiple numbers until they decide to quit by typing 'q'. 
The program includes error handling to ensure valid input and provides 
feedback when the user enters invalid data or negative integers.
"""

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

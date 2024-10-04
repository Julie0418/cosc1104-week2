"""
Author: Sarvesh More and Julekha Khatoon
Date: 2024-10-4
Description: This script defines a function to check if a given number is positive.
It continuously prompts the user for input, allowing them to check multiple numbers 
until they decide to quit by typing 'q'. The program handles invalid inputs gracefully 
and provides feedback to the user regarding the positivity of the entered number.
"""

# is_positive.py

def is_positive(number):
    return number > 0

if __name__ == "__main__":
    running = True  # Control the loop with this flag
    
    while running:
        user_input = input("Enter a number to check if it is positive (or type 'q' to quit): ")
        
        if user_input.lower() == 'q':
            print("Exiting program.")
            running = False  # Set flag to False to stop the loop
        else:
            try:
                number = float(user_input)
                result = is_positive(number)
                print(f"The number {number} is positive: {result}")
            except ValueError:
                print("Invalid input. Please enter a valid number or 'q' to quit.")

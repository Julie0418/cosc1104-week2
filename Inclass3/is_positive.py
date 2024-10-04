"""
Author: Sarvesh More and Julekha Khatoon
Date: 2024-10-4
Description: This script defines a function to check if a given number is positive.
"""

# is_positive.py

def is_positive(number):
    return number > 0

if __name__ == "__main__":
    print(is_positive(5))  # True
    print(is_positive(-3))  # False
    print(is_positive(0))  # False

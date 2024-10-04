"""
Author: Sarvesh More and Julekha Khatoon
Date: 2024-10-4
Description: This script defines a function to calculate the sum of the digits of a 
positive integer.
"""
# sum_of_digits.py

def sum_of_digits(number):
    return sum(int(digit) for digit in str(abs(number)))

if __name__ == "__main__":
    print(sum_of_digits(1234))  # 10
    print(sum_of_digits(9876))  # 30
    print(sum_of_digits(-246))  # 12

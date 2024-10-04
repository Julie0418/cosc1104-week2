"""
Author: Sarvesh More and Julekha Khatoon
Date: 2024-10-4
Description: This script provides functions to convert between Gibibytes and Gigabytes. 
"""
# conversions.py

def gibi_to_giga(gibibytes):
    return gibibytes * (1_073_741_824 / 1_000_000_000)

def giga_to_gibi(gigabytes):
    return gigabytes * (1_000_000_000 / 1_073_741_824)

if __name__ == "__main__":
    print(gibi_to_giga(1))  # 1.0737...
    print(gibi_to_giga(5))  # 5.3687...
    print(giga_to_gibi(1))  # 0.9313...
    print(giga_to_gibi(5))  # 4.6566...
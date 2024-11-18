import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Function to validate date format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%m-%d-%Y')  # Try to parse as MM-DD-YYYY
        return True
    except ValueError:
        return False

# Function to add a new expense
def add_expense(date, category, amount):
    # Validate date format (MM-DD-YYYY)
    if not is_valid_date(date):
        print("Invalid date format. Please use MM-DD-YYYY format.")
        return
    
    # Ensure the date is in MM/DD/YYYY format before saving
    date = datetime.strptime(date, '%m-%d-%Y').strftime('%m/%d/%Y')
    
    # Validate amount (must be a positive number)
    try:
        amount = float(amount)
        if amount <= 0:
            print("Amount must be a positive number.")
            return
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return
    
    # Write expense to CSV file
    with open('expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
    print("Expense added successfully!")

# Function to validate the expense category (non-empty)
def is_valid_category(category):
    if not category.strip():
        print("Category cannot be empty.")
        return False
    return True

# Function to view all expenses
def view_expenses():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                print(f"Date: {row[0]}, Category: {row[1]}, Amount: {row[2]}")
    except FileNotFoundError:
        print("No expenses recorded yet.")

# Function to plot the expenses
def plot_expenses():
    dates = []
    amounts = []
    
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                try:
                    # Try to parse the date with both MM/DD/YYYY and MM-DD-YYYY formats
                    date = datetime.strptime(row[0], '%m/%d/%Y')
                except ValueError:
                    date = datetime.strptime(row[0], '%m-%d-%Y')  # If it fails, try the second format
                
                dates.append(date)
                amounts.append(float(row[2]))  # Ensure the amount is a float

        # Sort by date to make sure the plot is in chronological order
        sorted_dates, sorted_amounts = zip(*sorted(zip(dates, amounts)))

        # Plotting the expenses
        plt.plot(sorted_dates, sorted_amounts, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Expenses Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ensure everything fits without overlap
        plt.show()

    except FileNotFoundError:
        print("No expenses recorded yet.")

# Function to check if the CSV file has a header and add it if missing
def check_and_add_header():
    try:
        with open('expenses.csv', 'r') as file:
            pass  # Just open the file to check if it exists
    except FileNotFoundError:
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount'])  # Add header

# Function to validate user menu choice
def is_valid_choice(choice):
    if choice not in ['1', '2', '3', '4', '5']:
        print("Invalid choice. Please enter a valid option (1/2/3/4/5).")
        return False
    return True

# Function to delete an expense
def delete_expense(date, category, amount):
    # Validate date format (MM-DD-YYYY)
    if not is_valid_date(date):
        print("Invalid date format. Please use MM-DD-YYYY format.")
        return
    
    # Ensure the date is in MM/DD/YYYY format before processing
    date = datetime.strptime(date, '%m-%d-%Y').strftime('%m/%d/%Y')
    
    # Read all rows from the CSV file
    expenses = []
    expense_found = False
    with open('expenses.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            # Check if the row matches the given expense
            if row[0] == date and row[1] == category and float(row[2]) == float(amount):
                expense_found = True
                continue  # Skip the row to "delete" it
            expenses.append(row)
    
    # If the expense was found, rewrite the CSV file without it
    if expense_found:
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount'])  # Re-add header
            writer.writerows(expenses)  # Write the remaining rows
        print(f"Expense on {date} for category '{category}' with amount {amount} deleted successfully!")
    else:
        print("Expense not found.")

# Main program function
def main():
    check_and_add_header()  # Ensure the CSV file has a header

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Plot Expenses")
        print("4. Delete Expense")
        print("5. Exit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")

        if not is_valid_choice(choice):
            continue  # Ask for a valid choice again
        
        if choice == '1':
            date = input("Enter the date (MM-DD-YYYY): ")
            category = input("Enter the category: ")
            if not is_valid_category(category):
                continue  # Ask for a valid category again
            amount = input("Enter the amount: ")
            add_expense(date, category, amount)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            plot_expenses()
        elif choice == '4':
            date = input("Enter the date (MM-DD-YYYY) of the expense to delete: ")
            category = input("Enter the category of the expense to delete: ")
            amount = input("Enter the amount of the expense to delete: ")
            delete_expense(date, category, amount)
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break

# Run the main program
if __name__ == "__main__":
    main()

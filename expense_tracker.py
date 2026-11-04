
import csv
from datetime import datetime
from pathlib import Path

FILE_NAME = Path("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]


# Create CSV file if it does not exist
def create_file():
    if not FILE_NAME.exists():
        with FILE_NAME.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


# Load all expenses
def load_expenses():
    create_file()
    with FILE_NAME.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# Save a new expense
def save_expense(expense):
    create_file()
    with FILE_NAME.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow(expense)


# Validate date
def get_valid_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date! Please try again.")


# Validate amount
def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return f"{amount:.2f}"

        except ValueError:
            print("Please enter a valid number.")


# Add expense
def add_expense():
    print("\n--- ADD EXPENSE ---")

    date = get_valid_date()

    category = input("Enter category: ").strip().title()

    while not category:
        print("Category cannot be empty.")
        category = input("Enter category: ").strip().title()

    description = input("Enter description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Enter description: ").strip()

    amount = get_valid_amount()

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    save_expense(expense)

    print("\nExpense saved successfully!")


# Display expenses
def display_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "-" * 75)
    print(f"{'DATE':<13}{'CATEGORY':<15}{'DESCRIPTION':<25}{'AMOUNT':>12}")
    print("-" * 75)

    for item in expenses:
        print(
            f"{item['date']:<13}"
            f"{item['category']:<15}"
            f"{item['description'][:23]:<25}"
            f"{float(item['amount']):>12.2f}"
        )

    print("-" * 75)


# View all expenses
def view_all_expenses():
    print("\n--- ALL EXPENSES ---")
    display_expenses(load_expenses())


# Filter expenses
def filter_expenses():
    expenses = load_expenses()

    print("\n1. Filter by Category")
    print("2. Filter by Month")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        category = input("Enter category: ").strip().lower()

        if not category:
            print("Category cannot be empty!")
            return

        filtered = [
            item for item in expenses
            if item["category"].lower() == category
        ]

    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")

            filtered = [
                item for item in expenses
                if item["date"].startswith(month)
            ]

        except ValueError:
            print("Invalid month format!")
            return

    else:
        print("Invalid choice!")
        return

    display_expenses(filtered)


# Category summary
def show_summary():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available.")
        return

    category_totals = {}
    grand_total = 0.0
    biggest_expense = None

    for item in expenses:
        amount = float(item["amount"])
        category = item["category"]

        category_totals[category] = (
            category_totals.get(category, 0.0) + amount
        )

        grand_total += amount

        if (
            biggest_expense is None
            or amount > float(biggest_expense["amount"])
        ):
            biggest_expense = item

    print("\n--- CATEGORY SUMMARY ---")

    for category, total in sorted(category_totals.items()):
        print(f"{category}: Rs. {total:.2f}")

    print(f"\nGrand Total: Rs. {grand_total:.2f}")

    print("\n--- BIGGEST EXPENSE ---")
    print("Date:", biggest_expense["date"])
    print("Category:", biggest_expense["category"])
    print("Description:", biggest_expense["description"])
    print("Amount: Rs.", biggest_expense["amount"])


# Main menu
def main():
    create_file()

    while True:
        print("\n================================")
        print("     PERSONAL EXPENSE TRACKER")
        print("================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses")
        print("4. Category Summary")
        print("5. Exit")
        print("================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_all_expenses()

        elif choice == "3":
            filter_expenses()

        elif choice == "4":
            show_summary()

        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()

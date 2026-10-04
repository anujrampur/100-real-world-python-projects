# Project 1: Personal Expense Tracker
# 100 Real-World Python Projects - Anuj Kumar Saxena
expenses = []


def add_expense():
    try:
        amount = float(input("Enter amount: "))
        if amount < 0:
            print("Amount cannot be negative.")
            return
        category = input("Enter category: ").strip()
        if not category:
            print("Category cannot be empty.")
            return
        expenses.append({"amount": amount, "category": category})
        print("Expense added successfully.")
    except ValueError:
        print("Please enter a valid amount.")


def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return
    for i, expense in enumerate(expenses, 1):
        print(f"{i}. {expense['category']}: {expense['amount']:.2f}")


def total_expense():
    print(f"Total Spending: {sum(e['amount'] for e in expenses):.2f}")


def category_summary():
    summary = {}
    for expense in expenses:
        cat = expense["category"]
        summary[cat] = summary.get(cat, 0) + expense["amount"]
    for category, amount in summary.items():
        print(f"{category}: {amount:.2f}")


def main():
    while True:
        print("\n1. Add Expense\n2. View Expenses\n3. Total Spending")
        print("4. Category Summary\n5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

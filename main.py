"""
main.py
-------
Entry point for the Personal Expense Tracker.
Provides an interactive command-line menu for all features.
"""

from datetime import datetime
from expense import Expense
from expense_manager import ExpenseManager
from report import ReportGenerator


# ── helpers ────────────────────────────────────────────────────────────

def print_menu() -> None:
    """Display the main menu."""
    print("""
╔══════════════════════════════════════════════╗
║        PERSONAL EXPENSE TRACKER              ║
╠══════════════════════════════════════════════╣
║  1.  Add Expense                             ║
║  2.  View All Expenses                       ║
║  3.  Edit Expense                            ║
║  4.  Delete Expense                          ║
║  5.  Filter by Category                      ║
║  6.  Filter by Date Range                    ║
║  7.  Search by Keyword                       ║
║  8.  Category-wise Summary                   ║
║  9.  Monthly Report                          ║
║  10. Highlights (Highest / Lowest)           ║
║  11. Full Report                             ║
║  0.  Exit                                    ║
╚══════════════════════════════════════════════╝""")


def get_category_choice() -> str:
    """Prompt user to pick a category from the list."""
    print("\n  Available categories:")
    for i, cat in enumerate(Expense.CATEGORIES, 1):
        print(f"    {i}. {cat}")

    while True:
        try:
            choice = int(input("  Enter category number: "))
            if 1 <= choice <= len(Expense.CATEGORIES):
                return Expense.CATEGORIES[choice - 1]
            print("  Invalid choice. Try again.")
        except ValueError:
            print("  Please enter a valid number.")


def get_positive_float(prompt: str) -> float:
    """Prompt until a valid positive number is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Amount must be positive.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid number.")


def get_date_input(prompt: str, allow_empty: bool = False) -> str | None:
    """Prompt for a date in YYYY-MM-DD format."""
    while True:
        date_str = input(prompt).strip()
        if allow_empty and date_str == "":
            return None
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("  Invalid date format. Use YYYY-MM-DD.")


def get_int_input(prompt: str) -> int:
    """Prompt until a valid integer is entered."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Please enter a valid integer.")


def display_expenses(expenses: list[Expense]) -> None:
    """Print a list of expenses in a readable table."""
    if not expenses:
        print("\n  No expenses found.")
        return
    print(f"\n  {'ID':<5} {'Date':<12} {'Amount':>10}   "
          f"{'Category':<15} {'Description'}")
    print("  " + "-" * 65)
    for e in expenses:
        print(f"  {e.id:<5} {e.date:<12} ₹{e.amount:>9.2f}   "
              f"{e.category:<15} {e.description}")
    print()


# ── menu actions ───────────────────────────────────────────────────────

def add_expense(manager: ExpenseManager) -> None:
    """Prompt user for details and add a new expense."""
    print("\n── Add New Expense ──")
    amount = get_positive_float("  Amount (₹): ")
    category = get_category_choice()
    description = input("  Description: ").strip()
    date = get_date_input("  Date (YYYY-MM-DD, leave blank for today): ",
                          allow_empty=True)

    try:
        expense = manager.add_expense(amount, category, description, date)
        print(f"\n  ✓ Expense added successfully!  →  {expense}")
    except ValueError as e:
        print(f"\n  ✗ Error: {e}")


def view_all(manager: ExpenseManager) -> None:
    """Show all expenses."""
    print("\n── All Expenses ──")
    expenses = manager.get_all_expenses()
    display_expenses(expenses)
    print(f"  Total: ₹{manager.total_expenses():.2f}  "
          f"({manager.count} expense(s))")


def edit_expense(manager: ExpenseManager) -> None:
    """Edit an existing expense."""
    print("\n── Edit Expense ──")
    exp_id = get_int_input("  Enter expense ID to edit: ")
    expense = manager.get_expense_by_id(exp_id)

    if expense is None:
        print(f"  ✗ No expense found with ID {exp_id}.")
        return

    print(f"  Current → {expense}")
    print("  (Press Enter to keep current value)\n")

    # amount
    amt_input = input(f"  New amount (current: ₹{expense.amount:.2f}): ").strip()
    # category
    print(f"  Current category: {expense.category}")
    cat_input = input("  Change category? (y/n): ").strip().lower()
    # description
    desc_input = input(f"  New description (current: {expense.description}): ").strip()
    # date
    date_input = input(f"  New date (current: {expense.date}): ").strip()

    kwargs = {}
    try:
        if amt_input:
            kwargs["amount"] = float(amt_input)
        if cat_input == "y":
            kwargs["category"] = get_category_choice()
        if desc_input:
            kwargs["description"] = desc_input
        if date_input:
            kwargs["date"] = date_input

        if not kwargs:
            print("  No changes made.")
            return

        manager.edit_expense(exp_id, **kwargs)
        print("  ✓ Expense updated successfully!")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def delete_expense(manager: ExpenseManager) -> None:
    """Delete an expense by ID."""
    print("\n── Delete Expense ──")
    exp_id = get_int_input("  Enter expense ID to delete: ")
    expense = manager.get_expense_by_id(exp_id)

    if expense is None:
        print(f"  ✗ No expense found with ID {exp_id}.")
        return

    print(f"  Found → {expense}")
    confirm = input("  Are you sure? (y/n): ").strip().lower()
    if confirm == "y":
        manager.delete_expense(exp_id)
        print("  ✓ Expense deleted.")
    else:
        print("  Cancelled.")


def filter_category(manager: ExpenseManager) -> None:
    """Filter expenses by category."""
    print("\n── Filter by Category ──")
    category = get_category_choice()
    results = manager.filter_by_category(category)
    print(f"\n  Showing expenses for: {category}")
    display_expenses(results)
    total = sum(e.amount for e in results)
    print(f"  Subtotal: ₹{total:.2f}  ({len(results)} expense(s))")


def filter_date_range(manager: ExpenseManager) -> None:
    """Filter expenses by date range."""
    print("\n── Filter by Date Range ──")
    start = get_date_input("  Start date (YYYY-MM-DD): ")
    end = get_date_input("  End date   (YYYY-MM-DD): ")
    results = manager.filter_by_date_range(start, end)
    print(f"\n  Showing expenses from {start} to {end}")
    display_expenses(results)
    total = sum(e.amount for e in results)
    print(f"  Subtotal: ₹{total:.2f}  ({len(results)} expense(s))")


def search_keyword(manager: ExpenseManager) -> None:
    """Search expenses by keyword in description."""
    print("\n── Search by Keyword ──")
    keyword = input("  Enter keyword: ").strip()
    if not keyword:
        print("  Please enter a keyword.")
        return
    results = manager.search(keyword)
    print(f"\n  Results for '{keyword}':")
    display_expenses(results)


# ── main loop ──────────────────────────────────────────────────────────

def main():
    """Run the expense tracker CLI."""
    manager = ExpenseManager()
    report = ReportGenerator(manager)

    actions = {
        "1": lambda: add_expense(manager),
        "2": lambda: view_all(manager),
        "3": lambda: edit_expense(manager),
        "4": lambda: delete_expense(manager),
        "5": lambda: filter_category(manager),
        "6": lambda: filter_date_range(manager),
        "7": lambda: search_keyword(manager),
        "8": lambda: print(report.category_report()),
        "9": lambda: print(report.monthly_report(
            get_int_input("  Year  (e.g. 2026): "),
            get_int_input("  Month (1-12): ")
        )),
        "10": lambda: print(report.highlights()),
        "11": lambda: print(report.full_report()),
    }

    print("\n  Welcome to the Personal Expense Tracker!")
    print("  Type a menu number to get started.\n")

    while True:
        print_menu()
        choice = input("\n  Enter your choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! Your expenses have been saved. 👋\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  Invalid choice. Please enter 0-11.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()

"""
expense_manager.py
------------------
Core class that manages the collection of expenses.
Provides methods for adding, deleting, editing, filtering,
and computing summaries over the expense data.
"""

from expense import Expense
from file_handler import FileHandler


class ExpenseManager:
    """Manages a collection of Expense objects with full CRUD operations.

    Uses a FileHandler internally for persistence (composition).
    """

    def __init__(self, filepath: str = "expenses.json"):
        self.__file_handler = FileHandler(filepath)
        self.__expenses: list[Expense] = self.__file_handler.load()
        self.__next_id: int = self._compute_next_id()

    # ---- private helpers -----------------------------------------------

    def _compute_next_id(self) -> int:
        """Determine the next available ID based on existing data."""
        if not self.__expenses:
            return 1
        return max(exp.id for exp in self.__expenses) + 1

    def _save(self) -> None:
        """Persist current state to disk."""
        self.__file_handler.save(self.__expenses)

    # ---- CRUD ----------------------------------------------------------

    def add_expense(self, amount: float, category: str,
                    description: str, date: str = None) -> Expense:
        """Create a new expense, add it to the list, and save."""
        expense = Expense(amount, category, description, date, self.__next_id)
        self.__expenses.append(expense)
        self.__next_id += 1
        self._save()
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by its ID. Returns True if found and removed."""
        for i, exp in enumerate(self.__expenses):
            if exp.id == expense_id:
                self.__expenses.pop(i)
                self._save()
                return True
        return False

    def edit_expense(self, expense_id: int, **kwargs) -> bool:
        """Edit fields of an existing expense.

        Accepted keyword arguments: amount, category, description, date.
        Returns True if the expense was found and updated.
        """
        expense = self.get_expense_by_id(expense_id)
        if expense is None:
            return False

        if "amount" in kwargs:
            expense.amount = kwargs["amount"]
        if "category" in kwargs:
            expense.category = kwargs["category"]
        if "description" in kwargs:
            expense.description = kwargs["description"]
        if "date" in kwargs:
            expense.date = kwargs["date"]

        self._save()
        return True

    # ---- retrieval & filtering -----------------------------------------

    def get_all_expenses(self) -> list[Expense]:
        """Return all expenses sorted by date (newest first)."""
        return sorted(self.__expenses, key=lambda e: e.date, reverse=True)

    def get_expense_by_id(self, expense_id: int) -> Expense | None:
        """Find a single expense by its ID."""
        for exp in self.__expenses:
            if exp.id == expense_id:
                return exp
        return None

    def filter_by_category(self, category: str) -> list[Expense]:
        """Return expenses that match the given category."""
        category = category.strip().title()
        return [e for e in self.__expenses if e.category == category]

    def filter_by_date_range(self, start: str, end: str) -> list[Expense]:
        """Return expenses within [start, end] (inclusive, YYYY-MM-DD)."""
        return [e for e in self.__expenses if start <= e.date <= end]

    def filter_by_month(self, year: int, month: int) -> list[Expense]:
        """Return expenses for a specific month."""
        prefix = f"{year}-{month:02d}"
        return [e for e in self.__expenses if e.date.startswith(prefix)]

    def search(self, keyword: str) -> list[Expense]:
        """Search expenses whose description contains the keyword."""
        keyword = keyword.lower()
        return [e for e in self.__expenses
                if keyword in e.description.lower()]

    # ---- calculations --------------------------------------------------

    def total_expenses(self) -> float:
        """Calculate the total of all expenses."""
        return round(sum(e.amount for e in self.__expenses), 2)

    def total_by_category(self) -> dict[str, float]:
        """Return a dictionary mapping each category to its total spend."""
        totals: dict[str, float] = {}
        for exp in self.__expenses:
            totals[exp.category] = totals.get(exp.category, 0) + exp.amount
        # sort by value descending
        return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))

    def monthly_total(self, year: int, month: int) -> float:
        """Calculate total expenses for a specific month."""
        return round(
            sum(e.amount for e in self.filter_by_month(year, month)), 2
        )

    def highest_expense(self) -> Expense | None:
        """Return the expense with the largest amount."""
        if not self.__expenses:
            return None
        return max(self.__expenses, key=lambda e: e.amount)

    def lowest_expense(self) -> Expense | None:
        """Return the expense with the smallest amount."""
        if not self.__expenses:
            return None
        return min(self.__expenses, key=lambda e: e.amount)

    @property
    def count(self) -> int:
        """Number of expenses currently stored."""
        return len(self.__expenses)

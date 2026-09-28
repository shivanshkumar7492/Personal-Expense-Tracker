"""
expense.py
----------
Defines the Expense data model with encapsulation.
Each expense has an id, amount, category, description, and date.
"""

from datetime import datetime


class Expense:
    """Represents a single expense entry.

    Attributes are kept private and accessed through properties
    to enforce validation (encapsulation).
    """

    CATEGORIES = [
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Health",
        "Education",
        "Other",
    ]

    def __init__(self, amount: float, category: str, description: str,
                 date: str = None, expense_id: int = None):
        self.amount = amount            # uses the property setter (validates)
        self.category = category        # uses the property setter (validates)
        self.__description = description
        self.__date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.__id = expense_id          # assigned by ExpenseManager

    # ---- properties (encapsulation) ------------------------------------

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        value = float(value)
        if value <= 0:
            raise ValueError("Amount must be a positive number.")
        self.__amount = round(value, 2)

    @property
    def category(self) -> str:
        return self.__category

    @category.setter
    def category(self, value: str):
        value = value.strip().title()
        if value not in self.CATEGORIES:
            raise ValueError(
                f"Invalid category '{value}'. "
                f"Choose from: {', '.join(self.CATEGORIES)}"
            )
        self.__category = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value: str):
        # validate date format
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        self.__date = value

    # ---- serialization -------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the expense to a dictionary (for JSON storage)."""
        return {
            "id": self.__id,
            "amount": self.__amount,
            "category": self.__category,
            "description": self.__description,
            "date": self.__date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Create an Expense instance from a dictionary."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data["date"],
            expense_id=data["id"],
        )

    # ---- display -------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"[{self.__id}]  {self.__date}  |  ₹{self.__amount:<10.2f}  |  "
            f"{self.__category:<15}  |  {self.__description}"
        )

    def __repr__(self) -> str:
        return (
            f"Expense(amount={self.__amount}, category='{self.__category}', "
            f"description='{self.__description}', date='{self.__date}', "
            f"expense_id={self.__id})"
        )

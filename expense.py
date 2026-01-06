# expense.py
# Defines the Expense data model

from datetime import datetime

class Expense:
    """
    Represents a single expense entry.
    """

    def __init__(self, date: str, category: str, amount: float, description: str):
        self.date = self._validate_date(date)
        self.category = self._validate_category(category)
        self.amount = self._validate_amount(amount)
        self.description = description.strip()

    @staticmethod
    def _validate_date(date_str: str) -> str:
        """
        Validates date format YYYY-MM-DD.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    @staticmethod
    def _validate_amount(amount: float) -> float:
        """
        Validates that the amount is positive.
        """
        if amount <= 0:
            raise ValueError("Expense amount must be positive.")
        return float(amount)

    @staticmethod
    def _validate_category(category: str) -> str:
        """
        Validates category string.
        """
        category = category.strip()
        if not category:
            raise ValueError("Category cannot be empty.")
        return category

    def to_dict(self) -> dict:
        """
        Converts the expense to a dictionary for Pandas/DataFrame usage.
        """
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }

    def __repr__(self) -> str:
        return (
            f"Expense(date={self.date}, "
            f"category={self.category}, "
            f"amount={self.amount:.2f}, "
            f"description={self.description})"
        )

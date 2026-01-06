# analytics.py
# Performs data analysis on expenses using Pandas and NumPy

import pandas as pd
import numpy as np
from tracker import ExpenseTracker

class ExpenseAnalytics:
    """
    Provides analytical operations on expense data.
    """

    def __init__(self, tracker: ExpenseTracker):
        self.tracker = tracker

    def _get_dataframe(self) -> pd.DataFrame:
        """
        Loads expenses and ensures correct data types.
        """
        df = self.tracker.get_all_expenses()
        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)
        return df

    def total_expenses(self) -> float:
        """
        Returns the total sum of all expenses.
        """
        df = self._get_dataframe()
        if df.empty:
            return 0.0
        return float(np.sum(df["amount"]))

    def average_daily_expenses(self) -> float:
        """
        Returns the average daily spending.
        """
        df = self._get_dataframe()
        if df.empty:
            return 0.0

        daily_totals = df.groupby(df["date"].dt.date)["amount"].sum()
        return float(np.mean(daily_totals))

    def expenses_by_category(self) -> pd.Series:
        """
        Returns total expenses grouped by category.
        """
        df = self._get_dataframe()
        if df.empty:
            return pd.Series(dtype=float)

        return df.groupby("category")["amount"].sum().sort_values(ascending=False)

    def monthly_totals(self) -> pd.Series:
        """
        Returns total expenses grouped by month.
        """
        df = self._get_dataframe()
        if df.empty:
            return pd.Series(dtype=float)

        return (
            df.groupby(df["date"].dt.to_period("M"))["amount"]
            .sum()
            .sort_index()
        )

    def highest_spending_category(self) -> str | None:
        """
        Returns the category with the highest total spending.
        """
        by_category = self.expenses_by_category()
        if by_category.empty:
            return None
        return by_category.idxmax()
# tracker.py
# Manages expense storage, loading, and saving

import os
import pandas as pd
from expense import Expense

class ExpenseTracker:
    """
    Handles adding, storing, loading, and retrieving expenses.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_storage()

    def _ensure_storage(self):
        """
        Ensures that the data directory and CSV file exist.
        """
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=["id", "date", "category", "amount", "description"])
            df.to_csv(self.file_path, index=False)

    def add_expense(self, date: str, category: str, amount: float, description: str):
        """
        Adds a new expense to the CSV file.
        """
        expense = Expense(date, category, amount, description)
        df = self._load_dataframe()
        
        # Generate ID
        if "id" in df.columns and not df.empty:
            max_id = df["id"].max()
            new_id = int(max_id + 1) if pd.notna(max_id) else 0
        else:
            new_id = 0
        
        expense_dict = expense.to_dict()
        expense_dict["id"] = new_id
        df = pd.concat([df, pd.DataFrame([expense_dict])], ignore_index=True)
        df.to_csv(self.file_path, index=False)

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Loads expenses from CSV into a DataFrame.
        """
        try:
            df = pd.read_csv(self.file_path)
            if df.empty or len(df.columns) == 0:
                return pd.DataFrame(columns=["id", "date", "category", "amount", "description"])
            
            # Migrate old files without ID
            if "id" not in df.columns:
                df.insert(0, "id", range(len(df)))
                df.to_csv(self.file_path, index=False)
            
            return df
        except (pd.errors.EmptyDataError, ValueError):
            return pd.DataFrame(columns=["id", "date", "category", "amount", "description"])

    def get_all_expenses(self) -> pd.DataFrame:
        """
        Returns all expenses as a Pandas DataFrame.
        """
        df = self._load_dataframe()
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df

    def filter_by_category(self, category: str) -> pd.DataFrame:
        """
        Returns expenses filtered by category.
        """
        df = self.get_all_expenses()
        if df.empty:
            return df
        return df[df["category"].str.lower() == category.lower()]

    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Returns expenses within a specific date range.
        """
        df = self.get_all_expenses()
        if df.empty:
            return df
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return df[(df["date"] >= start) & (df["date"] <= end)]

    def delete_expense(self, expense_id: int) -> bool:
        """
        Deletes an expense by its ID from the CSV file.
        """
        df = self._load_dataframe()
        if df.empty or "id" not in df.columns:
            return False
        
        initial_len = len(df)
        df = df[df["id"] != expense_id]
        
        if len(df) < initial_len:
            df.to_csv(self.file_path, index=False)
            return True
        return False

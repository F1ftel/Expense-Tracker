# tracker.py
# Parvalda izdevumu glabasanu, ieladi un saglabasanu
# Maksims Selkovskis ms24100, Raimonds Silinevics rs24085

import os # darbam ar failu celiem un direktorijiem
import pandas as pd # datu apstradei un CSV failu darbibam
from expense import Expense # atsevisku izdevumu validesanai un attelosanai

class ExpenseTracker:
    """
    Apstrada izdevumu pievienosanu, glabasanu, ieladi un izgusanu.
    """

    def __init__(self, file_path: str): # konstruktora metode, kas tiek izsaukta, kad tiek izveidots ExpenseTracker objekts
        self.file_path = file_path # saglaba celu uz CSV failu, kura tiek saglabati izdevumi
        self._ensure_storage() # parliecinas, ka direktorijs un CSV fails pastav

    def _ensure_storage(self):
        """
        Parliecinas, ka datu direktorijs un CSV fails pastav.
        """

        directory = os.path.dirname(self.file_path) # izvelk direktorijas celu no faila cela

        if directory and not os.path.exists(directory): # ja direktorija cels pastav un direktorijs vel nepastav, izveido direktoriju (ieskaitot vecaku direktorijus, ja nepieciesams)
            os.makedirs(directory)

        if not os.path.exists(self.file_path): # Ja CSV fails neeksiste, izveido tuksu CSV failu
            df = pd.DataFrame(columns=["id", "date", "category", "amount", "description"]) # izveido tuksu DataFrame ar ieprieks definetam kolonnam
            df.to_csv(self.file_path, index=False) # saglaba tukso DataFrame CSV faila

    def add_expense(self, date: str, category: str, amount: float, description: str):
        """
        Pievieno jaunu izdevumu CSV failam.
        """

        expense = Expense(date, category, amount, description) # izveido Expense objektu, kas automatiski parbauda ievadi

        df = self._load_dataframe() # ielade esosos izdevumus DataFrame

        if "id" in df.columns and not df.empty: # genere unique ID jaunajam izdevumam
            max_id = df["id"].max() # atrod maksimalo esoso ID
            new_id = int(max_id + 1) if pd.notna(max_id) else 0 # pieskir nakamo ID (apstrada NaN, ja nu gadijuma)
        else:
            new_id = 0 # ja DataFrame ir tukss vai trukst ID kolonnas, sak no 0
        
        expense_dict = expense.to_dict() # parveido izdevumu objektu vardnica
        expense_dict["id"] = new_id # pievieno genereto ID izdevumu vardnicai

        df = pd.concat([df, pd.DataFrame([expense_dict])], ignore_index=True) # pievieno jauno izdevumu DataFrame
        df.to_csv(self.file_path, index=False) # saglaba atjauninato DataFrame atpakal CSV faila

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Ielade izdevumus no CSV uz DataFrame.
        """

        try:
            df = pd.read_csv(self.file_path) # megina nolasit CSV failu uz DataFrame

            if df.empty or len(df.columns) == 0: # ja DataFrame ir tukss vai taja nav kolonnu, atgriez jaunu DataFrame ar pareizu strukturu
                return pd.DataFrame(columns=["id", "date", "category", "amount", "description"])

            if "id" not in df.columns: # apstrada migraciju no vecakiem CSV failiem bez ID kolonnas
                df.insert(0, "id", range(len(df))) # ievieto ID kolonnu pirmaja pozicija
                df.to_csv(self.file_path, index=False) # saglaba migreto DataFrame atpakal uz CSV
            
            return df # atgriez derigu DataFrame

        except ValueError: # ja fails ir tukss vai bojats, atgriez tiru DataFrame
            return pd.DataFrame(columns=["id", "date", "category", "amount", "description"])

    def get_all_expenses(self) -> pd.DataFrame:
        """
        Atgriez visus izdevumus ka Pandas DataFrame.
        """

        df = self._load_dataframe() # ielade DataFrame no CSV

        if not df.empty and "date" in df.columns: # konverte kolonnu "date" uz datuma/laika formatu, ja tada pastav
            df["date"] = pd.to_datetime(df["date"])

        return df

    def filter_by_category(self, category: str) -> pd.DataFrame:
        """
        Atgriez izdevumus, kas filtreti pec kategorijas.
        """

        df = self.get_all_expenses() # ielade visus izdevumus

        if df.empty: # ja nav izdevumu, atgriez tuksu DataFrame
            return df

        return df[df["category"].str.lower() == category.lower()] # filtre rindas, kuras atbilst kategorija (case-insensitive).

    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Atgriez izdevumus noteikta datumu diapazona.
        """

        df = self.get_all_expenses() # ielade visus izdevumus

        if df.empty: # ja nav izdevumu, atgriez tuksu DataFrame
            return df

        # parveido sakuma un beigu datumus par datetime objektiem
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        return df[(df["date"] >= start) & (df["date"] <= end)] # atgriez izdevumus noraditaja datumu diapazona

    def delete_expense(self, expense_id: int) -> bool:
        """
        Izdzes izdevumu pec ta ID no CSV faila.
        """

        df = self._load_dataframe() # ielade esoso DataFrame

        if df.empty or "id" not in df.columns: # ja DataFrame ir tukss vai trukst ID kolonnas, dzesana nav iespejama
            return False
        
        initial_len = len(df) # saglaba sakotnejo rindu skaitu

        df = df[df["id"] != expense_id] # nonem rindu ar noradito ID
        
        if len(df) < initial_len: # ja rinda tika nonemta, saglaba izmainas un atgriez True
            df.to_csv(self.file_path, index=False)
            return True

        return False # ja neviena rinda netika nonemta, atgriez False
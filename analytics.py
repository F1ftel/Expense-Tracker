# analytics.py
# Veic datu analizi par izdevumiem, izmantojot Pandas un NumPy
# Maksims Selkovskis ms24100, Raimonds Silinevics rs24085

import pandas as pd # datu manipulesanai un darbam ar DataFrame
import numpy as np # skaitliskam darbibam
from tracker import ExpenseTracker # mijiedarbibai ar izdevumu datiem

class ExpenseAnalytics:
    """
    Nodrosina analitiskas darbibas ar izdevumu datiem.
    """

    def __init__(self, tracker: ExpenseTracker): # lai mijiedarbotos ar izdevumu datiem
        self.tracker = tracker # saglaba ExpenseTracker izmantosanai saja klase

    def _get_dataframe(self) -> pd.DataFrame:
        """
        Ielade izdevumus un nodrosina pareizus datu tipus.
        """

        df = self.tracker.get_all_expenses() # iegust visus izdevumus no izsekotaja (atgriez pandas DataFrame)

        if df.empty: # ja nav izdevumu (tukss DataFrame), atgriez tuksu DataFrame
            return df

        df["date"] = pd.to_datetime(df["date"]) # vai kolonna 'date' ir datuma/laika formata, lai ar to butu viegli stradat

        df["amount"] = df["amount"].astype(float) # vai kolonna 'amount' ir float, lai veiktu skaitliskas darbibas, piemeram, summu un videjo vertibu

        return df # atgriez iztirito DataFrame

    def total_expenses(self) -> float: # metode kopejo izdevumu (kolonnas 'amount' summas) aprekinasanai
        """
        Atgriez visu izdevumu kopsummu.
        """

        df = self._get_dataframe() # ielade izdevumu datus

        if df.empty: # ja nav izdevumu, atgriez 0.0 ka kopsummu
            return 0.0
        
        return float(np.sum(df["amount"])) # apkopo kolonnu 'amount' un atgriez to ka float

    def average_daily_expenses(self) -> float:
        """
        Atgriez videjos dienas terinus.
        """

        df = self._get_dataframe() # ielade izdevumu datus

        if df.empty: # ja nav izdevumu, atgriez 0.0 ka videjo vertibu
            return 0.0

        daily_totals = df.groupby(df["date"].dt.date)["amount"].sum() # grupe datus pec datuma (dienas) un summe katras dienas izdevumus

        return float(np.mean(daily_totals)) # aprekina un atgriez dienas kopsummu videjo vertibu ka float

    def expenses_by_category(self) -> pd.Series:
        """
        Atgriez kopejos izdevumus, kas sagrupeti pa kategorijam.
        """

        df = self._get_dataframe() # ielade izdevumu datus

        if df.empty: # ja izdevumu nav, atgriez tuksu Series
            return pd.Series(dtype=float)

        return df.groupby("category")["amount"].sum().sort_values(ascending=False) # grupe datus pec 'category' un summe izdevumus katrai kategorijai, pec tam karto pec summas

    def monthly_totals(self) -> pd.Series:
        """
        Atgriez kopejos izdevumus, kas sagrupeti pa menesiem.
        """

        df = self._get_dataframe() # ielade izdevumu datus

        if df.empty: # ja izdevumu nav, atgriez tuksu Series
            return pd.Series(dtype=float)

        return ( # grupe datus pa menesiem (izmantojot 'to_period("M")', lai iegutu menesa periodus) un summejiet katra menesa izdevumus
            df.groupby(df["date"].dt.to_period("M"))["amount"]
            .sum()
            .sort_index() # karto pec perioda indeksa (kas ir menesis)
        )

    def highest_spending_category(self) -> str | None:
        """
        Atgriez kategoriju ar vislielakajiem kopejiem izdevumiem.
        """

        by_category = self.expenses_by_category() # iegust kopejos izdevumus pa kategorijam

        if by_category.empty: # ja nav izdevumu, atgriez None, jo nav kategorijas, par kuru zinot
            return None

        return by_category.idxmax() # atgriez kategoriju ar maksimalajiem kopejiem izdevumiem
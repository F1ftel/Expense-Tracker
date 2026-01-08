# expense.py
# Define izdevumu datu modeli
# Maksims Selkovskis ms24100, Raimonds Silinevics rs24085

from datetime import datetime # lai validetu un parsetu datumu virknes

class Expense:
    """
    Attelo vienu izdevumu ierakstu.
    """

    def __init__(self, date: str, category: str, amount: float, description: str): # konstruktora metode inicialize objekta atributus
        self.date = self._validate_date(date) # valide datuma virkni un saglaba to, ja ta ir deriga (atbilst formatam YYYY-MM-DD)
        self.category = self._validate_category(category) # valide un saglaba izdevumu kategoriju (novers tuksas vai whitespace-only kategorijas)
        self.amount = self._validate_amount(amount) # valide un saglaba izdevumu summu (nodrosina, ka summa ir pozitiva un skaitliska)
        self.description = description.strip() # nonem sakuma/aizmugures space no apraksta un saglaba to ka virkni

    @staticmethod # staticmethod, jo ta nav atkariga no instances mainigajiem
    def _validate_date(date_str: str) -> str:
        """
        Valide datuma formatu YYYY-MM-DD.
        """

        try: # megina parset datuma virkni, izmantojot nepieciesamo formatu (ja parsesana ir veiksmiga, atgriez sakotnejo datuma virkni)
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    @staticmethod
    def _validate_amount(amount: float) -> float:
        """
        Parbauda, ​​vai summa ir pozitivs skaitlis.
        """

        if amount <= 0: # parbauda, ​​vai summa ir mazaka vai vienada ar nulli (izveido kludu, ja summa nav deriga)
            raise ValueError("Expense amount must be positive.")

        return float(amount)

    @staticmethod
    def _validate_category(category: str) -> str:
        """
        Parbauda kategorijas virkni.
        """

        category = category.strip() # nonem sakuma un beigu space no kategorijas virknes

        if not category: # parbauda, ​​vai kategorija ir tuksa pec space nonemsanas (izraisa kludu, ja kategorija ir nederiga)
            raise ValueError("Category cannot be empty.")

        return category

    def to_dict(self) -> dict:
        """
        Parveido izdevumus par vardnicu Pandas/DataFrame lietosanai.
        """

        return { # atgriez vardnicu, kura atslegas atbilst CSV/DataFrame kolonnu nosaukumiem
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }

    def __repr__(self) -> str: # nosaka, ka Izdevumu objekts tiek attelots, kad tas tiek drukats vai registrets
        return (
            f"Expense(date={self.date}, "
            f"category={self.category}, "
            f"amount={self.amount:.2f}, "
            f"description={self.description})"
        )
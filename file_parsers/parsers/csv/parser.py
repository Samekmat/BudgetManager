from abc import ABC, abstractmethod

from django.contrib.auth.models import User


class BankCSVParsers(ABC):
    def __init__(self):
        self.incomes = []
        self.expenses = []

    @abstractmethod
    def parse_csv(self, csv_path: str, user: User):
        """Abstract method to parse CSV data for a specific bank and create
        Incomes/Expenses included.

        Parameters:
        - csv_path: str, path of the CSV data to be parsed.
        - user: User object, the currently logged-in user.

        Returns:
        - List of the transactions as an Income/Expense objects
        """
        pass

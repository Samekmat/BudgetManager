import csv
from abc import ABC, abstractmethod
from datetime import datetime

from expenses.models import Expense
from helper_models.models import Category, Currency
from incomes.models import Income


class BankCSVParsers(ABC):
    def __init__(self):
        self.incomes = []
        self.expenses = []

    @abstractmethod
    def parse_csv(self, csv_data, user):
        """Abstract method to parse CSV data for a specific bank and create
        Incomes/Expenses included.

        Parameters:
        - csv_data: str, the CSV data to be parsed.
        - user: User object, the currently logged-in user.

        Returns:
        - List of the transactions as a Income/Expense objects
        """
        pass


class SantanderParser(BankCSVParsers):
    def parse_csv(self, csv_path, user):
        income_category = Category.objects.get(type="income", name="CSV income import")
        expense_category = Category.objects.get(type="expense", name="CSV expense import")

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)

            for i, row in enumerate(csv_reader):
                if i == 0:
                    currency_code = row[4]
                    currency = Currency.objects.get(code=currency_code)
                    pass

                if not row:
                    continue

                try:
                    amount = row[5]
                    raw_date = row[1]

                    date = datetime.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")

                    amount_value = float(amount.replace(",", "."))
                    if amount_value >= 0:
                        transaction = Income(
                            user=user,
                            amount=amount_value,
                            date=date,
                            currency=currency,
                            category=income_category,
                        )
                        self.incomes.append(transaction)
                    else:
                        transaction = Expense(
                            user=user,
                            amount=abs(amount_value),
                            date=date,
                            currency=currency,
                            category=expense_category,
                        )
                        self.expenses.append(transaction)

                except Currency.DoesNotExist:
                    print(f"Error: Currency with code '{currency_code}' does not exist. Skipping line {i + 1}")
                    continue

                except (IndexError, ValueError) as e:
                    print(f"Error parsing line {i + 1}: {e}")
                    continue

                except Exception as e:
                    print(f"Unexpected error parsing line {i + 1}: {e}")
                    continue

            Income.objects.bulk_create(self.incomes)
            Expense.objects.bulk_create(self.expenses)

        return [self.incomes, self.expenses]

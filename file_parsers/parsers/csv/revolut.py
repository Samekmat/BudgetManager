import csv
from datetime import datetime
from typing import List, Tuple

from django.contrib.auth.models import User

from budget_manager_app.consts import CATEGORY__EXPENSE, CATEGORY__INCOME
from expenses.models import Expense
from file_parsers.parsers.csv.parser import BankCSVParsers
from helper_models.models import Category, Currency
from incomes.models import Income


class RevolutCSVParser(BankCSVParsers):
    """CSV Parser for Revolut bank statements.

    This class extends BankCSVParsers and provides a specific implementation for parsing
    Revolut bank statements in CSV format.
    """

    def parse_csv(self, csv_path: str, user: User) -> Tuple[List[Income], List[Expense]]:
        """Parse a Revolut bank statement in CSV format and import the transactions as
        Income and Expense objects.

        Args:
        - csv_path (str): The path to the CSV file.
        - user: The user for whom the transactions are imported.

        Returns:
        - Tuple[List[Income], List[Expense]]: A tuple containing lists of Income and Expense objects created during the import.
        """

        income_category = Category.objects.get(type=CATEGORY__INCOME, name="CSV income import")
        expense_category = Category.objects.get(type=CATEGORY__EXPENSE, name="CSV expense import")

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)

            for line_number, row in enumerate(csv_reader):
                if line_number == 0:
                    pass

                if not row:
                    continue

                try:
                    amount = row[5]
                    raw_date = row[2]
                    currency_code = row[7]
                    currency = Currency.objects.get(code=currency_code)

                    date = datetime.strptime(raw_date.split()[0], "%Y-%m-%d").strftime("%Y-%m-%d")

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
                    print(
                        f"Error: Currency with code '{currency_code}' does not exist. Skipping line {line_number + 1}"
                    )
                    continue

                except (IndexError, ValueError) as e:
                    print(f"Error parsing line {line_number + 1}: {e}")
                    continue

                except Exception as e:
                    print(f"Unexpected error parsing line {line_number + 1}: {e}")
                    continue

            Income.objects.bulk_create(self.incomes)
            Expense.objects.bulk_create(self.expenses)

        return self.incomes, self.expenses

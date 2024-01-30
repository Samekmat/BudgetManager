import csv
from datetime import datetime

from budget_manager_app.consts import CATEGORY__EXPENSE, CATEGORY__INCOME
from expenses.models import Expense
from file_parsers.parsers.csv.parser import BankCSVParsers
from helper_models.models import Category, Currency
from incomes.models import Income


class NestCSVParser(BankCSVParsers):
    def parse_csv(self, csv_path, user):
        income_category = Category.objects.get(type=CATEGORY__INCOME, name="CSV income import")
        expense_category = Category.objects.get(type=CATEGORY__EXPENSE, name="CSV expense import")

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)

            for line_number, row in enumerate(csv_reader):
                if line_number in range(0, 6):
                    pass

                if not row:
                    continue

                try:
                    amount = row[3]
                    raw_date = row[1]
                    currency_code = row[4]
                    currency = Currency.objects.get(code=currency_code)

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

from django.contrib.auth.models import User
from django.db import models

from expenses.models import Expense
from helper_models.models import Currency
from incomes.models import Income
from saving_goals.models import SavingGoal


class Budget(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="budgets",
        help_text="User who owns the budget",
    )
    shared_with = models.ManyToManyField(
        User,
        related_name="shared_budgets",
        blank=True,
        help_text="Users with whom the budget is shared",
    )
    incomes = models.ManyToManyField(Income)
    expenses = models.ManyToManyField(Expense)
    goals = models.ManyToManyField(SavingGoal, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    @property
    def calculate_balance(self):
        total_income = sum(income.amount for income in self.incomes.all())
        total_expense = sum(expense.amount for expense in self.expenses.all())

        total_result = total_income - total_expense
        return total_result

    class Meta:
        ordering = ["-id"]

from django.contrib.auth.models import User
from django.db import models

from helper_models.models import Currency

from expenses.models import Expense
from incomes.models import Income


class SavingGoal(models.Model):
    name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets',
                             help_text="User who owns the budget")
    shared_with = models.ManyToManyField(User, related_name='shared_budgets', blank=True,
                                         help_text="Users with whom the budget is shared")
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
        ordering = ['-id']

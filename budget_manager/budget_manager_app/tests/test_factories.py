from budget_manager_app.factories import BudgetFactory
from budget_manager_app.models import Budget
from django.contrib.auth.models import User
from django.test import TestCase
from expenses.models import Expense
from helper_models.models import Currency
from incomes.models import Income
from saving_goals.models import SavingGoal


class BudgetFactoryTest(TestCase):
    def test_create_budget_correct_create_object(self):
        BudgetFactory()

        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Currency.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Income.objects.count(), 2)
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(SavingGoal.objects.count(), 2)

    def test_create_budget_factory_batch_size_works_correctly(self):
        BudgetFactory.create_batch(5)

        self.assertEqual(Budget.objects.count(), 5)
        self.assertEqual(Currency.objects.count(), 5)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Income.objects.count(), 10)
        self.assertEqual(Expense.objects.count(), 10)
        self.assertEqual(SavingGoal.objects.count(), 10)

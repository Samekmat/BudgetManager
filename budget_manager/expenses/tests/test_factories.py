from django.contrib.auth.models import User
from django.test import TestCase
from expenses.factories import ExpenseFactory
from expenses.models import Expense
from helper_models.models import Category, Currency


# TODO
class ExpenseFactoryTest(TestCase):
    def test_create_expense_correct_create_object(self):
        ExpenseFactory()

        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Currency.objects.count(), 1)
        self.assertEqual(User.objects.count(), 3)

    def test_create_expense_factory_batch_size_works_correctly(self):
        ExpenseFactory.create_batch(5)

        self.assertEqual(Expense.objects.count(), 5)
        self.assertEqual(Category.objects.count(), 5)
        self.assertEqual(Currency.objects.count(), 5)
        self.assertEqual(User.objects.count(), 15)

from django.test import TestCase
from expenses.factories import ExpenseFactory
from expenses.forms import ExpenseForm


class ExpenseFormTestCase(TestCase):
    def setUp(self):
        self.expense = ExpenseFactory()

    def test_expense_form_valid_data(self):
        expense_data = {
            "amount": self.expense.amount,
            "date": self.expense.date,
            "category": self.expense.category.id,
            "payment_method": self.expense.payment_method,
            "currency": self.expense.currency.id,
            "user": self.expense.user,
        }
        form = ExpenseForm(data=expense_data)
        self.assertTrue(form.is_valid())

    def test_expense_form_invalid_data(self):
        expense_data_invalid = {
            "amount": -100,  # Invalid amount negative number
            "date": self.expense.date,
            "category": self.expense.category.id,
            "payment_method": self.expense.payment_method,
            "currency": self.expense.currency.id,
            "user": self.expense.user,
        }
        form = ExpenseForm(data=expense_data_invalid)
        self.assertFalse(form.is_valid())

    def test_expense_form_empty_data(self):
        expense_data_empty = {
            "amount": "",
            "date": "",
            "category": "",
            "payment_method": "",
            "currency": "",
            "user": "",
        }
        form = ExpenseForm(data=expense_data_empty)
        self.assertFalse(form.is_valid())

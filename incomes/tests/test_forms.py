from django.test import TestCase

from incomes.factories import IncomeFactory
from incomes.forms import IncomeForm


class IncomeFormTestCase(TestCase):
    def setUp(self):
        self.income = IncomeFactory()

    def test_income_form_valid_data(self):
        income_data = {
            "amount": self.income.amount,
            "date": self.income.date,
            "category": self.income.category.id,
            "payment_method": self.income.payment_method,
            "currency": self.income.currency.id,
            "user": self.income.user,
        }
        form = IncomeForm(data=income_data)
        self.assertTrue(form.is_valid())

    def test_income_form_invalid_data(self):
        income_data_invalid = {
            "amount": -10,
            "date": self.income.date,
            "category": self.income.category.id,
            "payment_method": self.income.payment_method,
            "currency": self.income.currency.id,
            "user": self.income.user,
        }
        form = IncomeForm(data=income_data_invalid)
        self.assertFalse(form.is_valid())

    def test_income_form_empty_data(self):
        income_data_empty = {
            "amount": "",
            "date": "",
            "category": "",
            "payment_method": "",
            "currency": "",
            "user": "",
        }
        form = IncomeForm(data=income_data_empty)
        self.assertFalse(form.is_valid())

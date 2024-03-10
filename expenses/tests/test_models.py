from django.test import TestCase

from expenses.factories import ExpenseFactory
from expenses.models import Expense
from helper_models.factories import TagFactory


class ExpensesModelTests(TestCase):
    def setUp(self):
        __tags = [TagFactory(), TagFactory()]

        self.expense = ExpenseFactory(tags=__tags)

    def test_expense_model(self):
        saved_expense = Expense.objects.get(pk=self.expense.pk)

        self.assertEqual(saved_expense.amount, self.expense.amount)
        self.assertEqual(saved_expense.date, self.expense.date)
        self.assertEqual(saved_expense.category, self.expense.category)
        self.assertEqual(saved_expense.user, self.expense.user)
        self.assertEqual(saved_expense.payment_method, "cash")
        self.assertEqual(saved_expense.currency, self.expense.currency)

        saved_tags = saved_expense.tags.all()
        self.assertEqual(saved_tags.count(), 2)

        expected_tag_names = saved_tags
        for i, tag in enumerate(saved_tags):
            self.assertEqual(tag.name, str(expected_tag_names[i]))

        expected_str = (
            f"Expense-{self.expense.pk}({self.expense.user}) - {self.expense.amount}{self.expense.currency.symbol}"
        )

        self.assertEqual(str(self.expense), expected_str)

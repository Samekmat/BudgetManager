from django.test import TestCase
from expenses.factories import ExpenseFactory
from expenses.models import Expense
from helper_models.factories import TagFactory


class ExpensesModelTests(TestCase):
    def setUp(self):
        # Initiate tags
        __tags = [TagFactory(), TagFactory()]

        # Use the ExpenseFactory to create an instance
        self.expense = ExpenseFactory(tags=__tags)

    def test_expense_model(self):
        # Retrieve the created expense from the database
        saved_expense = Expense.objects.get(pk=self.expense.pk)

        # Perform assertions to test the model fields
        self.assertEqual(saved_expense.amount, self.expense.amount)
        self.assertEqual(saved_expense.date, self.expense.date)
        self.assertEqual(saved_expense.category, self.expense.category)
        self.assertEqual(saved_expense.user, self.expense.user)
        self.assertEqual(saved_expense.payment_method, "cash")  # Default value from the factory
        self.assertEqual(saved_expense.currency, self.expense.currency)

        # Check the tags associated with the expense
        saved_tags = saved_expense.tags.all()
        self.assertEqual(saved_tags.count(), 2)  # Adjust the count based on factory

        # Check the names of the tags
        expected_tag_names = saved_tags
        for i, tag in enumerate(saved_tags):
            self.assertEqual(tag.name, str(expected_tag_names[i]))

        # Construct the expected string representation
        expected_str = f"Expense({self.expense.pk}) - {self.expense.amount}{self.expense.currency.symbol}"

        # Check if the __str__ method returns the expected value
        self.assertEqual(str(self.expense), expected_str)

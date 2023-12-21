from django.test import TestCase
from helper_models.factories import TagFactory
from incomes.factories import IncomeFactory
from incomes.models import Income


class IncomesModelTests(TestCase):
    def setUp(self):
        # Initiate tags
        __tags = [TagFactory(), TagFactory()]

        # Use the IncomeFactory to create an instance
        self.income = IncomeFactory(tags=__tags)

    def test_income_model(self):
        # Retrieve the created income from the database
        saved_income = Income.objects.get(pk=self.income.pk)

        # Perform assertions to test the model fields
        self.assertEqual(saved_income.amount, self.income.amount)
        self.assertEqual(saved_income.date, self.income.date)
        self.assertEqual(saved_income.category, self.income.category)
        self.assertEqual(saved_income.user, self.income.user)
        self.assertEqual(saved_income.payment_method, "cash")  # Default value from the factory
        self.assertEqual(saved_income.currency, self.income.currency)

        # Check the tags associated with the income
        saved_tags = saved_income.tags.all()
        self.assertEqual(saved_tags.count(), 2)  # Adjust the count based on factory

        # Optionally, check the names of the tags
        expected_tag_names = ["test tag 0", "test tag 1"]
        for i, tag in enumerate(saved_tags):
            self.assertEqual(tag.name, expected_tag_names[i])

        # Construct the expected string representation
        expected_str = f"Income({self.income.pk}) - {self.income.amount}{self.income.currency.symbol}"

        # Check if the __str__ method returns the expected value
        self.assertEqual(str(self.income), expected_str)

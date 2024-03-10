from django.test import TestCase

from helper_models.factories import TagFactory
from incomes.factories import IncomeFactory
from incomes.models import Income


class IncomesModelTests(TestCase):
    def setUp(self):
        __tags = [TagFactory(), TagFactory()]

        self.income = IncomeFactory(tags=__tags)

    def test_income_model(self):
        saved_income = Income.objects.get(pk=self.income.pk)

        self.assertEqual(saved_income.amount, self.income.amount)
        self.assertEqual(saved_income.date, self.income.date)
        self.assertEqual(saved_income.category, self.income.category)
        self.assertEqual(saved_income.user, self.income.user)
        self.assertEqual(saved_income.payment_method, "cash")
        self.assertEqual(saved_income.currency, self.income.currency)

        saved_tags = saved_income.tags.all()
        self.assertEqual(saved_tags.count(), 2)

        expected_tag_names = saved_tags
        for i, tag in enumerate(saved_tags):
            self.assertEqual(tag.name, str(expected_tag_names[i]))

        expected_str = (
            f"Income-{self.income.pk}({self.income.user}) - {self.income.amount}{self.income.currency.symbol}"
        )

        self.assertEqual(str(self.income), expected_str)

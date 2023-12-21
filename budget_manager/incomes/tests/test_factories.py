from django.contrib.auth.models import User
from django.test import TestCase
from helper_models.models import Category, Currency, Tag
from incomes.factories import IncomeFactory
from incomes.models import Income


class IncomeFactoryTest(TestCase):
    def test_create_income_correct_create_object(self):
        IncomeFactory()

        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Currency.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)
        self.assertEqual(User.objects.count(), 4)  # 1-income 1-category 2-tag

    def test_create_income_factory_batch_size_works_correctly(self):
        IncomeFactory.create_batch(5)

        self.assertEqual(Income.objects.count(), 5)
        self.assertEqual(Category.objects.count(), 5)
        self.assertEqual(Currency.objects.count(), 5)
        self.assertEqual(Tag.objects.count(), 10)
        self.assertEqual(User.objects.count(), 20)  # 5-income 5-category 10-tag

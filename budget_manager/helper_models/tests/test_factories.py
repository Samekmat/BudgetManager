from django.contrib.auth.models import User
from django.test import TestCase
from helper_models.factories import (
    CategoryExpenseFactory,
    CategoryIncomeFactory,
    CurrencyFactory,
    TagFactory,
)
from helper_models.models import Category, Currency, Tag


class CurrencyFactoriesTest(TestCase):
    def test_create_currency_correct_create_object(self):
        CurrencyFactory()

        self.assertEqual(Currency.objects.count(), 1)

    def test_create_currency_factory_batch_size_works_correctly(self):
        CurrencyFactory.create_batch(5)

        self.assertEqual(Currency.objects.count(), 5)


class CategoryFactoriesTest(TestCase):
    def test_create_category_correct_create_object(self):
        CategoryIncomeFactory()
        CategoryExpenseFactory()

        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(User.objects.count(), 2)

    def test_create_category_factory_batch_size_works_correctly(self):
        CategoryIncomeFactory.create_batch(5)
        CategoryExpenseFactory.create_batch(5)

        self.assertEqual(Category.objects.count(), 10)
        self.assertEqual(User.objects.count(), 10)


class TagFactoriesTest(TestCase):
    def test_create_tag_correct_create_object(self):
        TagFactory()

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)

    def test_create_tag_factory_batch_size_works_correctly(self):
        TagFactory.create_batch(5)

        self.assertEqual(Tag.objects.count(), 5)
        self.assertEqual(User.objects.count(), 5)

from django.test import Client, TestCase
from helper_models.factories import (
    CategoryExpenseFactory,
    CategoryIncomeFactory,
    CurrencyFactory,
    TagFactory,
)
from helper_models.models import Category, Currency, Tag
from users.factories import UserFactory


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category_income = CategoryIncomeFactory(user=self.user)
        self.category_expense = CategoryExpenseFactory(user=self.user)
        self.client = Client()

    def test_category_creation(self):
        saved_category_income = Category.objects.get(pk=self.category_income.pk)
        self.assertEqual(saved_category_income.name, self.category_income.name)
        self.assertEqual(saved_category_income.description, self.category_income.description)
        self.assertEqual(saved_category_income.type, self.category_income.type)
        self.assertFalse(saved_category_income.builtin)
        self.assertEqual(saved_category_income.user, self.user)

        saved_category_expense = Category.objects.get(pk=self.category_expense.pk)
        self.assertEqual(saved_category_expense.name, self.category_expense.name)
        self.assertEqual(saved_category_expense.description, self.category_expense.description)
        self.assertEqual(saved_category_expense.type, self.category_expense.type)
        self.assertFalse(saved_category_expense.builtin)
        self.assertEqual(saved_category_expense.user, self.user)

    def test_get_categories_for_user_authenticated(self):
        self.client.force_login(self.user)

        categories = Category.get_categories_for_user(self.user)
        self.assertEqual(categories.count(), 2)  # 1-category_income 1-category_expense

    def test_get_categories_for_user_unauthenticated(self):
        categories = Category.get_categories_for_user(None)
        self.assertEqual(categories.count(), 0)


class CurrencyModelTest(TestCase):
    def setUp(self):
        self.currency = CurrencyFactory()

    def test_currency_creation(self):
        saved_currency = Currency.objects.get(pk=self.currency.pk)
        self.assertEqual(saved_currency.name, self.currency.name)
        self.assertEqual(saved_currency.code, self.currency.code)
        self.assertEqual(saved_currency.symbol, self.currency.symbol)


class TagModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.tag = TagFactory(user=self.user)

    def test_tag_creation(self):
        saved_tag = Tag.objects.get(user=self.user)
        self.assertEqual(str(saved_tag), self.tag.name)
        self.assertEqual(saved_tag.user, self.user)

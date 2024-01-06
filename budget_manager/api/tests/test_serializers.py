from api.serializers import (
    CategorySerializer,
    ExpenseSerializer,
    IncomeSerializer,
    TagSerializer,
)
from django.test import TestCase
from expenses.factories import ExpenseFactory
from helper_models.factories import (
    CategoryExpenseFactory,
    CategoryIncomeFactory,
    TagFactory,
)
from incomes.factories import IncomeFactory
from users.factories import UserFactory


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.income = IncomeFactory(user=self.user)
        self.expense = ExpenseFactory(user=self.user)
        self.category_income = CategoryIncomeFactory(user=self.user)
        self.category_expense = CategoryExpenseFactory(user=self.user)
        self.tag = TagFactory(user=self.user)

    def test_income_serializer(self):
        serializer = IncomeSerializer(data=IncomeSerializer(self.income).data)
        self.assertTrue(serializer.is_valid())

    def test_expense_serializer(self):
        serializer = ExpenseSerializer(data=ExpenseSerializer(self.expense).data)
        self.assertTrue(serializer.is_valid())

    def test_category_serializer(self):
        serializer_cat_inc = CategorySerializer(data=CategorySerializer(self.category_income).data)
        serializer_cat_exp = CategorySerializer(data=CategorySerializer(self.category_expense).data)
        self.assertTrue(serializer_cat_inc.is_valid())
        self.assertTrue(serializer_cat_exp.is_valid())

    def test_tag_serializer(self):
        serializer = TagSerializer(data=TagSerializer(self.tag).data)
        self.assertTrue(serializer.is_valid())

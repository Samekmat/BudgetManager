from django.test import TestCase
from django.urls import resolve, reverse

from api.views import (
    CategoryDeleteAPIView,
    ExpenseDeleteAPIView,
    IncomeDeleteAPIView,
    TagDeleteAPIView,
)
from expenses.factories import ExpenseFactory
from helper_models.factories import CategoryIncomeFactory, TagFactory
from incomes.factories import IncomeFactory


class ApiUrlsTestCase(TestCase):
    def setUp(self):
        self.income = IncomeFactory()
        self.expense = ExpenseFactory()
        self.category = CategoryIncomeFactory()
        self.tag = TagFactory()

        self.income_url = reverse("api-income-delete", kwargs={"pk": self.income.id})
        self.expense_url = reverse("api-expense-delete", kwargs={"pk": self.expense.id})
        self.category_url = reverse("api-category-delete", kwargs={"pk": self.category.id})
        self.tag_url = reverse("api-tag-delete", kwargs={"pk": self.tag.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.income_url).func.view_class, IncomeDeleteAPIView)
        self.assertEqual(resolve(self.expense_url).func.view_class, ExpenseDeleteAPIView)
        self.assertEqual(resolve(self.category_url).func.view_class, CategoryDeleteAPIView)
        self.assertEqual(resolve(self.tag_url).func.view_class, TagDeleteAPIView)

    def test_urls_reverse(self):
        self.assertEqual(self.income_url, f"/api/incomes/{self.income.id}/delete/")
        self.assertEqual(self.expense_url, f"/api/expenses/{self.expense.id}/delete/")
        self.assertEqual(self.category_url, f"/api/categories/{self.category.id}/delete/")
        self.assertEqual(self.tag_url, f"/api/tags/{self.tag.id}/delete/")

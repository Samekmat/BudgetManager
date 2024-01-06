from django.test import TestCase
from django.urls import reverse
from expenses.factories import ExpenseFactory
from helper_models.factories import (
    CategoryExpenseFactory,
    CategoryIncomeFactory,
    TagFactory,
)
from incomes.factories import IncomeFactory
from rest_framework import status
from rest_framework.test import APIClient
from users.factories import UserFactory


class APIViewsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.income = IncomeFactory(user=self.user)
        self.expense = ExpenseFactory(user=self.user)
        self.category_income = CategoryIncomeFactory(user=self.user)
        self.category_expense = CategoryExpenseFactory(user=self.user)
        self.tag = TagFactory(user=self.user)

        self.client = APIClient()
        self.client_unauthenticated = APIClient()

        self.client.force_authenticate(user=self.user)

    def test_income_delete_api(self):
        url = reverse("api-income-delete", kwargs={"pk": self.income.pk})

        response_unauthenticated = self.client_unauthenticated.delete(url)
        self.assertEqual(response_unauthenticated.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_expense_delete_api(self):
        url = reverse("api-expense-delete", kwargs={"pk": self.expense.pk})

        response_unauthenticated = self.client_unauthenticated.delete(url)
        self.assertEqual(response_unauthenticated.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_delete_api(self):
        url_income = reverse("api-category-delete", kwargs={"pk": self.category_income.pk})
        url_expense = reverse("api-category-delete", kwargs={"pk": self.category_expense.pk})

        response_income_unauthenticated = self.client_unauthenticated.delete(url_income)
        self.assertEqual(response_income_unauthenticated.status_code, status.HTTP_403_FORBIDDEN)

        response_expense_unauthenticated = self.client_unauthenticated.delete(url_expense)
        self.assertEqual(response_expense_unauthenticated.status_code, status.HTTP_403_FORBIDDEN)

        response_income = self.client.delete(url_income)
        response_expense = self.client.delete(url_expense)
        self.assertEqual(response_income.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_expense.status_code, status.HTTP_204_NO_CONTENT)

    def test_tag_delete_api(self):
        url = reverse("api-tag-delete", kwargs={"pk": self.tag.pk})

        response_unauthenticated = self.client_unauthenticated.delete(url)
        self.assertEqual(response_unauthenticated.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from http import HTTPStatus

from budget_manager_app.factories import BudgetFactory
from budget_manager_app.forms import IncomeExpenseSelectForm
from budget_manager_app.models import Budget
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from expenses.factories import ExpenseFactory
from incomes.factories import IncomeFactory
from users.factories import UserFactory


class BudgetViewsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.budget = BudgetFactory(user=self.user)

        self.client = Client()
        self.client.force_login(self.user)

        self.list_url = reverse("budgets:budgets")
        self.create_url = reverse("budgets:budget-create")
        self.update_url = reverse("budgets:budget-update", kwargs={"pk": self.budget.id})
        self.delete_url = reverse("budgets:budget-delete", kwargs={"pk": self.budget.id})
        self.add_income_expense_url = reverse("budgets:add-income-expense", kwargs={"budget_id": self.budget.id})
        self.chart_url = reverse("budgets:budget-chart", kwargs={"budget_id": self.budget.id})
        self.dashboard_url = reverse("dashboard")

        self.other_user = UserFactory(username="otheruser", email="otheruser@user.com", password="ZAQ!2wsx")
        self.budget.shared_with.add(self.other_user)
        self.income = IncomeFactory(user=self.user)
        self.expense = ExpenseFactory(user=self.other_user)

        self.factory = RequestFactory()

    def test_budget_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.budget.name)

    def test_budget_create_view(self):
        response = self.client.post(self.create_url, self.budget.__dict__, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Budget.objects.filter(name=self.budget.name, user=self.user).exists())

    def test_budget_update_view(self):
        response = self.client.post(self.update_url, self.budget.__dict__, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Budget.objects.filter(name=self.budget.name, user=self.user).exists())

    def test_budget_delete_view(self):
        response = self.client.post(self.delete_url, self.budget.__dict__, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Budget.objects.filter(name=self.budget.name, user=self.user).exists())

    def test_budget_delete_view_permission_denied(self):
        self.client.logout()
        self.client.force_login(self.other_user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(Budget.objects.filter(pk=self.budget.pk).exists())
        self.assertContains(
            response, "You don't have permission to delete this budget", status_code=HTTPStatus.FORBIDDEN
        )

    def test_budget_add_income_expense_view_get_with_permissions(self):
        response = self.client.get(self.add_income_expense_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context["form"], IncomeExpenseSelectForm)
        self.assertEqual(response.context["budget"], self.budget)

    def test_budget_add_income_expense_view_post_valid_form(self):
        data = {"incomes": [self.income.id], "expenses": [self.expense.id]}
        response = self.client.post(self.add_income_expense_url, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.list_url)

        self.budget.refresh_from_db()
        self.assertIn(self.income, self.budget.incomes.all())
        self.assertIn(self.expense, self.budget.expenses.all())

    def test_budget_add_income_expense_view_post_invalid_form(self):
        data = {}
        response = self.client.post(self.add_income_expense_url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_chart_view(self):
        response = self.client.get(self.chart_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_dashboard_view(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

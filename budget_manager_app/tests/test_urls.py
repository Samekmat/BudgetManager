from django.test import TestCase
from django.urls import resolve, reverse

from budget_manager_app.factories import BudgetFactory
from budget_manager_app.views import (
    BudgetCreateView,
    BudgetDeleteView,
    BudgetListView,
    BudgetUpdateView,
)


class BudgetUrlsTestCase(TestCase):
    def setUp(self):
        self.budget = BudgetFactory()

        self.list_url = reverse("budgets:budgets")
        self.create_url = reverse("budgets:budget-create")
        self.update_url = reverse("budgets:budget-update", kwargs={"pk": self.budget.id})
        self.delete_url = reverse("budgets:budget-delete", kwargs={"pk": self.budget.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.list_url).func.view_class, BudgetListView)
        self.assertEqual(resolve(self.create_url).func.view_class, BudgetCreateView)
        self.assertEqual(resolve(self.update_url).func.view_class, BudgetUpdateView)
        self.assertEqual(resolve(self.delete_url).func.view_class, BudgetDeleteView)

    def test_urls_reverse(self):
        self.assertEqual(self.list_url, "/budgets/")
        self.assertEqual(self.create_url, "/budgets/create/")
        self.assertEqual(self.update_url, f"/budgets/{self.budget.id}/update/")
        self.assertEqual(self.delete_url, f"/budgets/{self.budget.id}/delete/")

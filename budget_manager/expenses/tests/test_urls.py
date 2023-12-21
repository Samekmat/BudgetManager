from django.test import TestCase
from django.urls import resolve, reverse
from expenses.factories import ExpenseFactory
from expenses.views import ExpenseCreateView, ExpenseListView, ExpenseUpdateView


class ExpenseUrlsTestcase(TestCase):
    def setUp(self):
        self.expense = ExpenseFactory()

        # Urls
        self.list_url = reverse("expenses:expenses")
        self.create_url = reverse("expenses:expense-create")
        self.update_url = reverse("expenses:expense-update", kwargs={"pk": self.expense.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.list_url).func.view_class, ExpenseListView)
        self.assertEqual(resolve(self.create_url).func.view_class, ExpenseCreateView)
        self.assertEqual(resolve(self.update_url).func.view_class, ExpenseUpdateView)

    def test_urls_reverse(self):
        self.assertEqual(self.list_url, "/expenses/expenses/")
        self.assertEqual(self.create_url, "/expenses/expenses/create/")
        self.assertEqual(self.update_url, f"/expenses/expenses/{self.expense.id}/update/")

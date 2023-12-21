from django.test import TestCase
from django.urls import resolve, reverse
from incomes.factories import IncomeFactory
from incomes.views import IncomeCreateView, IncomeListView, IncomeUpdateView


class IncomeUrlsTestcase(TestCase):
    def setUp(self):
        self.income = IncomeFactory()

        # Urls
        self.list_url = reverse("incomes:incomes")
        self.create_url = reverse("incomes:income-create")
        self.update_url = reverse("incomes:income-update", kwargs={"pk": self.income.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.list_url).func.view_class, IncomeListView)
        self.assertEqual(resolve(self.create_url).func.view_class, IncomeCreateView)
        self.assertEqual(resolve(self.update_url).func.view_class, IncomeUpdateView)

    def test_urls_reverse(self):
        self.assertEqual(self.list_url, "/incomes/incomes/")
        self.assertEqual(self.create_url, "/incomes/incomes/create/")
        self.assertEqual(self.update_url, f"/incomes/incomes/{self.income.id}/update/")

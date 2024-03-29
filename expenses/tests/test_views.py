from decimal import Decimal

from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import Client, TestCase
from django.urls import reverse

from expenses.factories import ExpenseFactory
from expenses.models import Expense
from users.factories import UserFactory


class ExpenseViewsTest(MessagesTestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.expense = ExpenseFactory(user=self.user)
        self.client = Client()

        self.list_url = reverse("expenses:expenses")
        self.create_url = reverse("expenses:expense-create")
        self.update_url = reverse("expenses:expense-update", kwargs={"pk": self.expense.id})

        self.client.force_login(self.user)

        self.other_user = UserFactory(username="otheruser", email="otheruser@user.com")

    def test_expense_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

        self.assertIn("expenses", response.context)
        expenses = response.context["expenses"]
        self.assertEqual(len(expenses), 1)

        filter_params = {
            "date": str(self.expense.date),
            "payment_method": self.expense.payment_method,
            "tags": self.expense.tags,
            "currency": self.expense.currency,
        }

        response_filter = self.client.get(self.list_url, filter_params)

        self.assertEqual(response_filter.status_code, 200)
        self.assertIn("expenses", response_filter.context)
        incomes_filter = response_filter.context["expenses"]
        self.assertEqual(len(incomes_filter), 1)

    def test_expense_create_view(self):
        expense_data = {
            "amount": self.expense.amount,
            "date": self.expense.date,
            "category": self.expense.category.id,
            "payment_method": self.expense.payment_method,
            "currency": self.expense.currency.id,
        }

        response = self.client.post(self.create_url, expense_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)

        created_income = Expense.objects.get(amount=self.expense.amount, user=self.user, id=self.expense.id)
        self.assertEqual(created_income.amount, self.expense.amount)
        self.assertEqual(created_income.date, self.expense.date)
        self.assertEqual(created_income.category, self.expense.category)
        self.assertEqual(created_income.payment_method, self.expense.payment_method)
        self.assertEqual(created_income.currency, self.expense.currency)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Expense created successfully.")])

    def test_expense_update_view(self):
        updated_expense_data = {
            "amount": self.expense.amount + Decimal(20),
            "date": self.expense.date,
            "category": self.expense.category.id,
            "payment_method": "credit_card",
            "currency": self.expense.currency.id,
        }

        response = self.client.post(self.update_url, updated_expense_data)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, self.list_url)

        updated_expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(updated_expense.amount, self.expense.amount + Decimal(20))
        self.assertEqual(updated_expense.date, self.expense.date)
        self.assertEqual(updated_expense.category, self.expense.category)
        self.assertEqual(updated_expense.payment_method, updated_expense_data["payment_method"])
        self.assertEqual(updated_expense.currency, self.expense.currency)

        self.assertMessages(response, [Message(level=25, message="Expense updated successfully.")])

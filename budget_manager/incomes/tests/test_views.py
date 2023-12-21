from decimal import Decimal

from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import Client, TestCase
from django.urls import reverse
from incomes.factories import IncomeFactory
from incomes.models import Income
from users.factories import UserFactory


class IncomeViewsTest(MessagesTestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.income = IncomeFactory(user=self.user)
        self.client = Client()

        # Urls
        self.list_url = reverse("incomes:incomes")
        self.create_url = reverse("incomes:income-create")
        self.update_url = reverse("incomes:income-update", kwargs={"pk": self.income.id})

        # Log in user
        self.client.force_login(self.user)

        # Create another user
        self.other_user = UserFactory(username="otheruser", email="otheruser@user.com", password="ZAQ!2wsx")

    def test_income_list_view(self):
        response = self.client.get(self.list_url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the incomes are present in the context
        self.assertIn("incomes", response.context)
        incomes = response.context["incomes"]
        self.assertEqual(len(incomes), 1)

        # Check with filter params given
        filter_params = {
            "date": str(self.income.date),
            "payment_method": self.income.payment_method,
            "tags": self.income.tags,
            "currency": self.income.currency,
        }

        response_filter = self.client.get(self.list_url, filter_params)

        self.assertEqual(response_filter.status_code, 200)
        self.assertIn("incomes", response_filter.context)
        incomes_filter = response_filter.context["incomes"]
        self.assertEqual(len(incomes_filter), 1)

    def test_income_create_view(self):
        # Use IncomeFactory to generate data
        income_data = {
            "amount": self.income.amount,
            "date": self.income.date,
            "category": self.income.category.id,
            "payment_method": self.income.payment_method,
            "currency": self.income.currency.id,
        }

        # Post the data to the create view
        response = self.client.post(self.create_url, income_data)

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)

        # Check that Income was created in db
        created_income = Income.objects.get(amount=self.income.amount, user=self.user, id=self.income.id)
        self.assertEqual(created_income.amount, self.income.amount)
        self.assertEqual(created_income.date, self.income.date)
        self.assertEqual(created_income.category, self.income.category)
        self.assertEqual(created_income.payment_method, self.income.payment_method)
        self.assertEqual(created_income.currency, self.income.currency)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Income created successfully.")])

    def test_income_update_view(self):
        updated_income_data = {
            "amount": self.income.amount + Decimal(20),
            "date": self.income.date,
            "category": self.income.category.id,
            "payment_method": "credit_card",
            "currency": self.income.currency.id,
        }

        # Post the updated form data to the update view
        response = self.client.post(self.update_url, updated_income_data)

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect URL is correct
        self.assertRedirects(response, self.list_url)

        # Check that the Income was updated in the database
        updated_income = Income.objects.get(id=self.income.id)
        self.assertEqual(updated_income.amount, self.income.amount + Decimal(20))
        self.assertEqual(updated_income.date, self.income.date)
        self.assertEqual(updated_income.category, self.income.category)
        self.assertEqual(updated_income.payment_method, updated_income_data["payment_method"])
        self.assertEqual(updated_income.currency, self.income.currency)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Income updated successfully.")])

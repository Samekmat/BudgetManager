from decimal import Decimal

from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.http import HttpResponseForbidden
from django.test import Client, TestCase
from django.urls import reverse
from saving_goals.factories import SavingGoalFactory
from saving_goals.models import SavingGoal
from users.factories import UserFactory


class SavingGoalViewsTest(MessagesTestMixin, TestCase):
    def setUp(self):
        # Create a user and a saving_goal using factories
        self.user = UserFactory()
        self.goal = SavingGoalFactory(user=self.user)
        self.client = Client()

        # Urls
        self.list_url = reverse("saving_goals:goals")
        self.create_url = reverse("saving_goals:goal-create")
        self.update_url = reverse("saving_goals:goal-update", kwargs={"pk": self.goal.id})
        self.detail_url = reverse("saving_goals:goal-detail", kwargs={"pk": self.goal.id})
        self.delete_url = reverse("saving_goals:goal-delete", kwargs={"pk": self.goal.id})

        # Log in user
        self.client.force_login(self.user)

        # Create another user
        self.other_user = UserFactory(username="otheruser", email="otheruser@user.com", password="ZAQ!2wsx")

    def test_saving_goal_list_view(self):
        response = self.client.post(self.list_url, {"amount_to_add": 200, "goal_id": self.goal.id})

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect URL is correct
        self.assertRedirects(response, reverse("saving_goals:goals"))

        # Check that the goal has been updated
        updated_goal = SavingGoal.objects.get(id=self.goal.id)
        self.assertEqual(updated_goal.amount, self.goal.amount + Decimal(200))

        # Check if the success message is present in the messages
        self.assertMessages(
            response,
            [Message(level=25, message="Added 200$ to the goal.")],
        )

        # Check error message if amount is negative
        response = self.client.post(self.list_url, {"amount_to_subtract": -5, "goal_id": self.goal.id})
        self.assertMessages(response, [Message(level=40, message="Invalid amount to subtract.")])

    def test_saving_goal_create_view(self):
        # Use SavingGoalFactory to generate form data
        saving_goal_data = {
            "name": self.goal.name,
            "amount": self.goal.amount,
            "goal": self.goal.goal,
            "currency": self.goal.currency.id,
        }

        # Post the form data to the create view
        response = self.client.post(self.create_url, saving_goal_data)

        # Check that the redirect URL is correct
        self.assertEqual(response.status_code, 302)

        # Check that redirect is correct
        self.assertRedirects(response, self.list_url)

        # Check that the SavingGoal was created in the database
        created_goal = SavingGoal.objects.get(name=self.goal.name, user=self.user, id=self.goal.id)
        self.assertEqual(created_goal.amount, self.goal.amount)
        self.assertEqual(created_goal.goal, self.goal.goal)
        self.assertEqual(created_goal.currency, self.goal.currency)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Saving goal created successfully.")])

    def test_saving_goal_update_view(self):
        # Use SavingGoalFactory to generate updated form data
        updated_saving_goal_data = {
            "name": "Updated Goal Name",
            "amount": self.goal.amount + Decimal(100),
            "goal": self.goal.goal + Decimal(50),
            "currency": self.goal.currency.id,
        }

        # Post the updated form data to the update view
        response = self.client.post(self.update_url, updated_saving_goal_data)
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect URL is correct
        self.assertRedirects(response, self.list_url)

        # Check that the SavingGoal was updated in the database
        updated_goal = SavingGoal.objects.get(id=self.goal.id)
        self.assertEqual(updated_goal.name, updated_saving_goal_data["name"])
        self.assertEqual(updated_goal.amount, self.goal.amount + Decimal(100))
        self.assertEqual(updated_goal.goal, self.goal.goal + Decimal(50))
        self.assertEqual(updated_goal.currency, self.goal.currency)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Saving goal updated successfully.")])

    def test_saving_goal_detail_view(self):
        # Check template used
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, "saving_goals/goal_detail.html")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.goal.name)

        # Logout previous user
        self.client.logout()

        # Test unauthenticated user redirect to login page
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, f"/users/login/?next={self.detail_url}")

        # Log in the other user
        self.client.force_login(self.other_user)

        # Ensure authenticated user cannot access other user's goal
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code)

    def test_delete_saving_goal_view(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(SavingGoal.objects.count(), 0)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Saving goal deleted successfully.")])

    def test_delete_view_permission_denied(self):
        # Logout previous user
        self.client.logout()

        # Log in the other user
        self.client.force_login(self.other_user)

        response = self.client.delete(self.delete_url)

        # Check that the response status code is 403 (forbidden)
        self.assertEqual(response.status_code, 403)

        # Check that the goal is not deleted
        self.assertTrue(SavingGoal.objects.filter(pk=self.goal.pk).exists())

        # Check the error message
        self.assertContains(response, "You don't have permission to delete this goal.", status_code=403)

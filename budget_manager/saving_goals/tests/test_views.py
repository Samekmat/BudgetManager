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
        self.user = UserFactory()
        self.goal = SavingGoalFactory(user=self.user)
        self.client = Client()

        # Urls
        self.list_url = reverse("saving_goals:goals")
        self.create_url = reverse("saving_goals:goal-create")
        self.update_url = reverse("saving_goals:goal-update", kwargs={"pk": self.goal.id})
        self.detail_url = reverse("saving_goals:goal-detail", kwargs={"pk": self.goal.id})
        self.delete_url = reverse("saving_goals:goal-delete", kwargs={"pk": self.goal.id})

        self.client.force_login(self.user)

        self.other_user = UserFactory(username="otheruser", email="otheruser@user.com", password="ZAQ!2wsx")

    def test_saving_goal_list_view(self):
        response = self.client.post(self.list_url, {"amount_to_add": 200, "goal_id": self.goal.id})

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse("saving_goals:goals"))

        updated_goal = SavingGoal.objects.get(id=self.goal.id)
        self.assertEqual(updated_goal.amount, self.goal.amount + Decimal(200))

        self.assertMessages(
            response,
            [Message(level=25, message="Added 200$ to the goal.")],
        )

        response = self.client.post(self.list_url, {"amount_to_subtract": -5, "goal_id": self.goal.id})
        self.assertMessages(response, [Message(level=40, message="Invalid amount to subtract.")])

    def test_saving_goal_create_view(self):
        saving_goal_data = {
            "name": self.goal.name,
            "amount": self.goal.amount,
            "goal": self.goal.goal,
            "currency": self.goal.currency.id,
        }

        response = self.client.post(self.create_url, saving_goal_data)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, self.list_url)

        created_goal = SavingGoal.objects.get(name=self.goal.name, user=self.user, id=self.goal.id)
        self.assertEqual(created_goal.amount, self.goal.amount)
        self.assertEqual(created_goal.goal, self.goal.goal)
        self.assertEqual(created_goal.currency, self.goal.currency)

        self.assertMessages(response, [Message(level=25, message="Saving goal created successfully.")])

    def test_saving_goal_update_view(self):
        updated_saving_goal_data = {
            "name": "Updated Goal Name",
            "amount": self.goal.amount + Decimal(100),
            "goal": self.goal.goal + Decimal(50),
            "currency": self.goal.currency.id,
        }

        response = self.client.post(self.update_url, updated_saving_goal_data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, self.list_url)

        updated_goal = SavingGoal.objects.get(id=self.goal.id)
        self.assertEqual(updated_goal.name, updated_saving_goal_data["name"])
        self.assertEqual(updated_goal.amount, self.goal.amount + Decimal(100))
        self.assertEqual(updated_goal.goal, self.goal.goal + Decimal(50))
        self.assertEqual(updated_goal.currency, self.goal.currency)

        self.assertMessages(response, [Message(level=25, message="Saving goal updated successfully.")])

    def test_saving_goal_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, "saving_goals/goal_detail.html")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.goal.name)

        self.client.logout()

        response = self.client.get(self.detail_url)
        self.assertRedirects(response, f"/users/login/?next={self.detail_url}")

        self.client.force_login(self.other_user)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code)

    def test_delete_saving_goal_view(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(SavingGoal.objects.count(), 0)

        self.assertMessages(response, [Message(level=25, message="Saving goal deleted successfully.")])

    def test_delete_view_permission_denied(self):
        self.client.logout()

        self.client.force_login(self.other_user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, 403)

        self.assertTrue(SavingGoal.objects.filter(pk=self.goal.pk).exists())

        self.assertContains(response, "You don't have permission to delete this goal.", status_code=403)

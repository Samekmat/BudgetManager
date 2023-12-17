from decimal import Decimal

from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import Client, TestCase
from django.urls import reverse
from saving_goals.factories import SavingGoalFactory
from saving_goals.models import SavingGoal
from users.factories import UserFactory


class SavingGoalViewTest(MessagesTestMixin, TestCase):
    def setUp(self):
        # Create a user and a saving_goal using factories
        self.user = UserFactory()
        self.goal = SavingGoalFactory(user=self.user)
        self.client = Client()

    def test_saving_goal_list_view(self):
        self.client.force_login(self.user)

        url = reverse("saving_goals:goals")
        response = self.client.post(url, {"amount_to_add": 200, "goal_id": self.goal.id})

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
        response = self.client.post(url, {"amount_to_subtract": -5, "goal_id": self.goal.id})
        self.assertMessages(response, [Message(level=40, message="Invalid amount to subtract.")])

    def test_saving_goal_create_view(self):
        self.client.force_login(self.user)

        url = reverse("saving_goals:goal-create")

        # Use SavingGoalFactory to generate form data
        saving_goal_data = {
            "name": self.goal.name,
            "amount": self.goal.amount,
            "goal": self.goal.goal,
            "currency": self.goal.currency,
        }

        # Post the form data to the create view
        response = self.client.post(url, saving_goal_data, follow=True)

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)

        # Check that the redirect URL is correct TODO
        # self.assertRedirects(response, reverse("saving_goals:goals"))

        # Check that the SavingGoal was created in the database
        created_goal = SavingGoal.objects.get(name=self.goal.name, user=self.user)
        self.assertEqual(created_goal.amount, self.goal.amount)
        self.assertEqual(created_goal.goal, self.goal.goal)
        self.assertEqual(created_goal.currency, self.goal.currency)

        # Check message TODO
        # self.assertMessages(
        #     response, [Message(level=25, message="Saving goal created successfully.")]
        # )

    def test_saving_goal_update_view(self):
        url = reverse("saving_goals:goal-update", kwargs={"pk": self.goal.id})

        # Use SavingGoalFactory to generate updated form data
        updated_saving_goal_data = {
            "name": "Updated Goal Name",
            "amount": self.goal.amount + Decimal(100),
            "goal": self.goal.goal + Decimal(50),
            "currency": self.goal.currency,
        }

        # Post the updated form data to the update view
        response = self.client.post(url, updated_saving_goal_data)
        # Check that the response is a redirect TODO
        # self.assertEqual(response.status_code, 302)
        #
        # # Check that the redirect URL is correct
        # self.assertRedirects(response, reverse('saving_goals:goals'))

        # Check that the SavingGoal was updated in the database
        updated_goal = SavingGoal.objects.get(id=self.goal.id)
        self.assertEqual(updated_goal.name, updated_saving_goal_data["name"])
        self.assertEqual(updated_goal.amount, self.goal.amount + Decimal(100))
        self.assertEqual(updated_goal.goal, self.goal.goal + Decimal(50))
        self.assertEqual(updated_goal.currency, self.goal.currency)

        # Check message
        self.assertMessages(response, [Message(level=25, message="Saving goal updated successfully.")])

from decimal import Decimal

from django.test import TestCase
from saving_goals.factories import SavingGoalFactory
from saving_goals.forms import SavingGoalForm


class SavingGoalFormTestCase(TestCase):
    def setUp(self):
        self.saving_goal = SavingGoalFactory()
        self.initial_amount = self.saving_goal.amount
        self.amount_to_add = Decimal("500.00")
        self.amount_to_subtract = Decimal("200.00")

    def test_saving_goal_form_valid_data(self):
        saving_goal_data = {
            "name": self.saving_goal.name,
            "amount": self.saving_goal.amount,
            "goal": self.saving_goal.goal,
            "currency": self.saving_goal.currency,
            "user": self.saving_goal.user,
        }
        form = SavingGoalForm(data=saving_goal_data)
        self.assertTrue(form.is_valid())

    def test_saving_goal_form_invalid_data(self):
        saving_goal_data_invalid = {
            "name": self.saving_goal.name,
            "amount": self.saving_goal.amount,
            "goal": -100,
            "currency": self.saving_goal.currency,
            "user": self.saving_goal.user,
        }

        form = SavingGoalForm(data=saving_goal_data_invalid)
        self.assertFalse(form.is_valid())

    def test_saving_goal_form_empty_data(self):
        saving_goal_data_empty = {
            "name": "",
            "amount": "",
            "goal": "",
            "currency": "",
            "user": "",
        }

        form = SavingGoalForm(data=saving_goal_data_empty)
        self.assertFalse(form.is_valid())

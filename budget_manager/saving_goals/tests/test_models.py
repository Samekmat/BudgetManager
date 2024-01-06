from decimal import Decimal

from django.db import DataError
from django.test import TestCase
from saving_goals.factories import SavingGoalFactory
from saving_goals.models import SavingGoal


class SavingGoalTestCase(TestCase):
    def setUp(self):
        self.test_goal = SavingGoalFactory()
        self.custom_goal = SavingGoalFactory(
            name="Default amount if not specified",
            amount=0,
        )
        self.wrong_goal = SavingGoalFactory(
            amount=-100,
            goal=-500,
        )

    def test_saving_goal_creation(self):
        self.assertIsInstance(self.test_goal, SavingGoal)
        self.assertEqual(self.test_goal.name, "default_goal")

    def test_saving_goal_goal_edge_cases(self):
        self.assertGreaterEqual(self.test_goal.goal, 0.00)
        self.assertLessEqual(self.test_goal.goal, 1000_000_000)

    def test_saving_goal_amount_validation(self):
        self.assertGreaterEqual(self.test_goal.amount, 0.00)
        self.assertLessEqual(self.test_goal.amount, 1000_000_000)

    def test_saving_goal_goal_precision(self):
        self.assertEqual(self.test_goal.goal, round(self.test_goal.goal, 2))

    def test_saving_goal_amount_precision(self):
        self.assertEqual(self.test_goal.amount, round(self.test_goal.amount, 2))

    def test_saving_goal_currency_relation(self):
        self.assertIsNotNone(self.test_goal.currency)

    def test_saving_goal_user_relation(self):
        self.assertIsNotNone(self.test_goal.user)

    def test_saving_goal_default_amount(self):
        self.assertEqual(self.custom_goal.amount, Decimal("0.00"))

    def test_saving_goal_name_constraints(self):
        self.assertTrue(len(self.test_goal.name) <= 120)

    def test_saving_goal_name_exceeds_max_length(self):
        with self.assertRaises(DataError):
            SavingGoalFactory(name="a" * 121)

    def test_saving_goal_str(self):
        self.assertEqual(str(self.test_goal), "default_goal")

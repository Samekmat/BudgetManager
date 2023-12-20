from django.contrib.auth.models import User
from django.test import TestCase, tag
from helper_models.models import Currency
from saving_goals.factories import SavingGoalFactory
from saving_goals.models import SavingGoal


@tag("x")
class SavingGoalFactoriesTest(TestCase):
    def test_create_saving_goal_correct_create_object(self):
        SavingGoalFactory()

        self.assertEqual(SavingGoal.objects.count(), 1)
        self.assertEqual(Currency.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)

    def test_create_saving_goal_factory_batch_size_works_correctly(self):
        SavingGoalFactory.create_batch(5)

        self.assertEqual(SavingGoal.objects.count(), 5)
        self.assertEqual(Currency.objects.count(), 5)
        self.assertEqual(User.objects.count(), 5)

from django.test import TestCase
from django.urls import resolve, reverse
from saving_goals.factories import SavingGoalFactory
from saving_goals.views import (
    SavingGoalCreateView,
    SavingGoalDeleteView,
    SavingGoalDetailView,
    SavingGoalListView,
    SavingGoalUpdateView,
)


class SavingGoalsUrlsTestCase(TestCase):
    def setUp(self):
        self.goal = SavingGoalFactory()

        # Urls
        self.list_url = reverse("saving_goals:goals")
        self.create_url = reverse("saving_goals:goal-create")
        self.update_url = reverse("saving_goals:goal-update", kwargs={"pk": self.goal.id})
        self.detail_url = reverse("saving_goals:goal-detail", kwargs={"pk": self.goal.id})
        self.delete_url = reverse("saving_goals:goal-delete", kwargs={"pk": self.goal.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.list_url).func.view_class, SavingGoalListView)
        self.assertEqual(resolve(self.create_url).func.view_class, SavingGoalCreateView)
        self.assertEqual(resolve(self.update_url).func.view_class, SavingGoalUpdateView)
        self.assertEqual(resolve(self.detail_url).func.view_class, SavingGoalDetailView)
        self.assertEqual(resolve(self.delete_url).func.view_class, SavingGoalDeleteView)

    def test_urls_reverse(self):
        self.assertEqual(self.list_url, "/goals/goals/")
        self.assertEqual(self.create_url, "/goals/goals/create/")
        self.assertEqual(self.update_url, f"/goals/goals/{self.goal.id}/update/")
        self.assertEqual(self.detail_url, f"/goals/goals/{self.goal.id}/detail/")
        self.assertEqual(self.delete_url, f"/goals/goals/{self.goal.id}/delete/")

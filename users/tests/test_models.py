from django.contrib.auth import get_user_model
from django.test import TestCase

from users.factories import UserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_creation(self):
        self.assertIsInstance(self.user, get_user_model())

        self.assertTrue(self.user.username)

        self.assertTrue(self.user.password)

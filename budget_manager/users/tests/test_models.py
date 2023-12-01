from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from users.factories import UserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_creation(self):
        self.assertIsInstance(self.user, get_user_model())

        # Check if the user has a non-empty username
        self.assertTrue(self.user.username)

        # Check if the password is correctly hashed
        self.assertTrue(check_password("ZAQ!2wsx", self.user.password))


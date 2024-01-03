from django.test import TestCase
from users.factories import UserFactory
from users.forms import LoginForm, RegisterForm


class RegisterFormTestCase(TestCase):
    def test_register_form_valid_data(self):
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password1": "test_pass_123",
            "password2": "test_pass_123",
        }
        form = RegisterForm(data=user_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        user_data_invalid = {
            "username": "test_user",
            "email": "invalid_email",  # Invalid email format
            "password1": "test_pass_123",
            "password2": "test_pass_123",
        }
        form_invalid = RegisterForm(data=user_data_invalid)
        self.assertFalse(form_invalid.is_valid())

    def test_register_form_save(self):
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = RegisterForm(data=user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@example.com")


class LoginFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_login_form_valid(self):
        form_data = {
            "username": self.user.username,
            "password": "ZAQ!2wsx",
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {"username": self.user.username, "password": "wrong_pass123!"}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

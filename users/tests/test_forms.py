from django.test import Client, TestCase
from django.urls import reverse

from users.factories import UserFactory
from users.forms import RegisterForm


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
            "email": "invalid_email",
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
        client = Client()
        response = client.post(reverse("users:login"), {"username": self.user.username, "password": "ZAQ!2wsx"})
        self.assertEqual(response.status_code, 302)  # Assuming successful login redirects to another page

    def test_login_form_invalid(self):
        client = Client()
        response = client.post(reverse("users:login"), {"username": self.user.username, "password": "wrong_pass123!"})
        self.assertEqual(response.status_code, 200)

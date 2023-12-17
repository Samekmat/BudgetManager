from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import Client, TestCase
from django.urls import reverse
from users.factories import UserFactory


class AuthenticationViewsTestCase(MessagesTestMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password="<RandomPassword>")

    def test_register_view(self):
        user_data = {
            "email": "test_user@gmail.com",
            "username": "test_user",
            "password1": "ZAQ!2wsx",
            "password2": "ZAQ!2wsx",
        }

        register_url = reverse("users:register")
        response = self.client.post(register_url, user_data)

        # Check if the user is redirected to the login page after successful registration
        self.assertRedirects(response, reverse("users:login"))

        # Check if the user is created
        self.assertTrue(User.objects.filter(username=user_data["username"]).exists())

        # Check if the user is logged in after registration
        user = authenticate(username=user_data["username"], password=user_data["password1"])
        self.assertIsNotNone(user)

        # Check if the success message is present in the messages
        self.assertMessages(
            response,
            [Message(level=25, message="Registration successful. You are now logged in.")],
        )

    def test_login_view(self):
        login_url = reverse("users:login")
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(**self.credentials)

        # User.objects.create(username='test_user', password='<PASSWORD>')
        # response = self.client.post(login_url, data={'username': 'test_user', 'password': '<PASSWORD>'})
        response = self.client.post(login_url, self.credentials)

        # Check if the user is redirected to the index page after successful login
        self.assertRedirects(response, reverse("index"), status_code=302, target_status_code=200)

        # Check if the user is actually logged in
        user = authenticate(**self.credentials)
        self.assertIsNotNone(user)

        # Check if the success message is present in the messages
        self.assertMessages(response, [Message(level=25, message="Login successful. Welcome back!")])

    def test_logout_view(self):
        # Log in user
        self.client.login(username=self.user.username, password=self.user.password)

        logout_url = reverse("users:logout")
        response = self.client.get(logout_url)

        # Check if the user is redirected to the login page after logout
        expected_redirect_url = reverse("users:login") + "?next=" + reverse("users:logout")
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

        # Check if the user is actually logged out
        user = authenticate(username=self.user.username, password=self.user.password)
        self.assertIsNone(user)

        # Check if the success message is present in the messages
        self.assertMessages(
            response,
            [Message(level=25, message="You have been successfully logged out.")],
        )

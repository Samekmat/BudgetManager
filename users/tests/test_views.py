from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from users.factories import UserFactory, generate_random_password


class AuthenticationViewsTestCase(MessagesTestMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.request_factory = RequestFactory()

    def test_register_view(self):
        password = generate_random_password()
        user_data = {
            "email": "test_user@gmail.com",
            "username": "test_user",
            "password1": password,
            "password2": password,
        }

        register_url = reverse("users:register")
        response = self.client.post(register_url, user_data)

        self.assertRedirects(response, reverse("users:login"))

        self.assertTrue(User.objects.filter(username=user_data["username"]).exists())

        request_register = self.request_factory.get(register_url)
        user = authenticate(request=request_register, username=user_data["username"], password=user_data["password1"])
        self.assertIsNotNone(user)

        self.assertMessages(
            response,
            [Message(level=25, message="Registration successful. You are now logged in.")],
        )

    def test_login_view(self):
        login_url = reverse("users:login")
        self.credentials = {"username": "testuser", "password": generate_random_password()}
        User.objects.create_user(**self.credentials)

        response = self.client.post(login_url, self.credentials)

        self.assertRedirects(response, reverse("index"), status_code=302, target_status_code=200)

        request_login = self.request_factory.get(login_url)
        user = authenticate(request=request_login, **self.credentials)
        self.assertIsNotNone(user)

        self.assertMessages(response, [Message(level=25, message="Login successful. Welcome!")])

    def test_logout_view(self):
        self.client.force_login(self.user)

        logout_url = reverse("users:logout")
        response = self.client.post(logout_url, follow=True)

        expected_redirect_url = reverse("users:login")
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

        request_logout = self.request_factory.get(logout_url)
        user = authenticate(request=request_logout, username=self.user.username, password=self.user.password)
        self.assertIsNone(user)

        self.assertMessages(
            response,
            [Message(level=25, message="You have been successfully logged out.")],
        )

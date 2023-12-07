from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from users.factories import UserFactory


class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()

    def test_register_view(self):
        user_data = {
            'username': 'test_user',
            'password1': 'ZAQ!2wsx',
            'password2': 'ZAQ!2wsx'
        }

        register_url = reverse('users:register')
        response = self.client.post(register_url, user_data)

        # Check if the user is redirected to the login page after successful registration
        self.assertRedirects(response, reverse('users:login'))

        # Check if the user is created
        self.assertTrue(User.objects.filter(username=user_data['username']).exists())

        # Check if the user is logged in after registration
        user = authenticate(username=user_data['username'], password=user_data['password1'])
        self.assertIsNotNone(user)

    def test_login_view(self):
        login_url = reverse('users:login')
        response = self.client.post(login_url, data={'username': self.user.username, 'password': self.user.password})

        # Check if the user is redirected to the index page after successful login
        self.assertRedirects(response, reverse('index'), status_code=302, target_status_code=200)

        # Check if the user is actually logged in
        user = authenticate(username=self.user.username, password=self.user.password)
        self.assertIsNotNone(user)

    def test_logout_view(self):
        # Log in user
        self.client.login(username=self.user.username, password=self.user.password)

        logout_url = reverse('users:logout')
        response = self.client.post(logout_url)

        # Check if the user is redirected to the login page after logout
        self.assertRedirects(response, reverse('users:login'), status_code=302, target_status_code=200)

        # Check if the user is actually logged out
        user = authenticate(username=self.user.username, password=self.user.password)
        self.assertIsNone(user)

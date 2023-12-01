from django.test import TestCase, Client
from django.urls import reverse

from users.factories import UserFactory


class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_register_view(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'test_user',
            'password1': 'ZAQ!2wsx',
            'password2': 'ZAQ!2wsx'
        })


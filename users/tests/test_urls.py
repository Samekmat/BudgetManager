from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import CustomLogoutView, LoginView, RegisterView


class UrlsTestCase(SimpleTestCase):
    def setUp(self):
        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")
        self.logout_url = reverse("users:logout")

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.register_url).func.view_class, RegisterView)
        self.assertEqual(resolve(self.login_url).func.view_class, LoginView)
        self.assertEqual(resolve(self.logout_url).func.view_class, CustomLogoutView)

    def test_urls_reverse(self):
        self.assertEqual(self.register_url, "/users/register/")
        self.assertEqual(self.login_url, "/users/login/")
        self.assertEqual(self.logout_url, "/users/logout/")

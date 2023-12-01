from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import RegisterView, LoginView, CustomLogoutView


class UrlsTestCase(SimpleTestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')

    def test_register_url_resolves(self):
        self.assertEqual(resolve(self.register_url).func.view_class, RegisterView)

    def test_login_url_resolves(self):
        self.assertEqual(resolve(self.login_url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        self.assertEqual(resolve(self.logout_url).func.view_class, CustomLogoutView)

    def test_register_reverse(self):
        self.assertEqual(self.register_url, '/users/register/')

    def test_login_reverse(self):
        self.assertEqual(self.login_url, '/users/login/')

    def test_logout_reverse(self):
        self.assertEqual(self.logout_url, '/users/logout/')

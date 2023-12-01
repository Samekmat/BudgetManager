from django.test import TestCase
from users.forms import RegisterForm, LoginForm
from users.factories import UserFactory


class RegisterFormTestCase(TestCase):
    def test_register_form(self):
        user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'test_pass_123',
            'password2': 'test_pass_123'
        }
        form = RegisterForm(data=user_data)
        self.assertTrue(form.is_valid())

    def test_register_form_save(self):
        user_data = {'username': 'test_user', 'email': 'test@example.com', 'password1': 'testpass123',
                     'password2': 'testpass123'}
        form = RegisterForm(data=user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')


class LoginFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_login_form_valid(self):
        form_data = {
            'username': self.user.username,
            'password': 'ZAQ!2wsx',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {
            'username': self.user.username,
            'password': 'wrong_pass123!'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

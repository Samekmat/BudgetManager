from django.contrib.auth.models import User
from django.test import TestCase

from users.factories import UserFactory
from users.models import Profile


class UsersFactoriesTestCase(TestCase):
    def test_create_user_factory_correct_create_object(self):
        UserFactory()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_user_factory_batch_size_works_correctly(self):
        UserFactory.create_batch(5)

        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Profile.objects.count(), 5)

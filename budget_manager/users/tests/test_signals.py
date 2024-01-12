from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from users.factories import UserFactory
from users.models import Profile
from users.signals import create_profile

User = get_user_model()


class ProfileSignalTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

        post_save.connect(create_profile, sender=User, dispatch_uid="test_create_profile_handler")

    def tearDown(self):
        post_save.disconnect(create_profile, sender=User, dispatch_uid="test_create_profile_handler")

    def test_profile_created_signal(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), f"Profile of {self.user.username}")

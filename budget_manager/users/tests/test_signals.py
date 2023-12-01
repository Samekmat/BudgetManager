from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from users.signals import create_profile
from users.factories import UserFactory
from users.models import Profile


class ProfileSignalTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        # Connect signal before the test
        post_save.connect(create_profile, sender=get_user_model(), dispatch_uid='test_create_profile_handler')

    def tearDown(self):
        # Disconnect the signal after the test
        post_save.disconnect(create_profile, sender=get_user_model(), dispatch_uid='test_create_profile_handler')

    def test_profile_created_signal(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), f"Profile of {self.user.username}")

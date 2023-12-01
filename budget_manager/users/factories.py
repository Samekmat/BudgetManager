import factory
from django.contrib.auth.hashers import make_password
from faker import Faker

from django.contrib.auth.models import User
from users.models import Profile


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.LazyAttribute(lambda _: make_password("ZAQ!2wsx"))


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

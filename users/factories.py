import random
import string

import factory
from django.contrib.auth.models import User
from faker import Faker

from users.models import Profile

fake = Faker()


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.LazyAttribute(lambda obj: generate_random_password())


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

import factory
from users.factories import UserFactory
from decimal import Decimal
from random import randint
from .models import SavingGoal

from helper_models.factories import CurrencyFactory


class SavingGoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavingGoal

    name = 'default_goal'
    amount = factory.LazyFunction(lambda: Decimal(randint(100, 10_000)))
    goal = factory.LazyFunction(lambda: Decimal(randint(500, 5000)))
    currency = factory.SubFactory(CurrencyFactory)
    user = factory.SubFactory(UserFactory)


currency = CurrencyFactory()
SavingGoalFactory.create(name='new computer', currency=currency)

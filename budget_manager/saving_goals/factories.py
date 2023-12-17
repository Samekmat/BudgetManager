from decimal import ROUND_DOWN, Decimal
from random import randint

import factory

from .models import SavingGoal


class SavingGoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavingGoal

    name = "default_goal"
    amount = factory.LazyFunction(
        lambda: Decimal(randint(0, 1000_000_000) / 100).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    )
    goal = factory.LazyFunction(
        lambda: Decimal(randint(0, 1000_000_000) / 100).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    )
    currency = factory.SubFactory("helper_models.factories.CurrencyFactory")
    user = factory.SubFactory("users.factories.UserFactory")

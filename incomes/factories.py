from datetime import date
from decimal import ROUND_DOWN, Decimal
from random import randint

import factory

from helper_models.factories import TagFactory

from .models import Income


class IncomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Income

    amount = factory.LazyFunction(
        lambda: Decimal(randint(0, 1000_000_000) / 100).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    )
    date = factory.LazyFunction(date.today)
    category = factory.SubFactory("helper_models.factories.CategoryIncomeFactory", user=factory.SelfAttribute("..user"))
    user = factory.SubFactory("users.factories.UserFactory")
    payment_method = "cash"
    currency = factory.SubFactory("helper_models.factories.CurrencyFactory")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Create specified tags
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Default: Create two tags
            self.tags.add(TagFactory(user=self.user))
            self.tags.add(TagFactory(user=self.user))

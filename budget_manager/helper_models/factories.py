import factory
from helper_models.models import Currency


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency

    name = "US Dollar"
    code = "USD"
    symbol = "$"

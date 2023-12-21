import factory
from helper_models.models import Category, Currency, Tag


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency

    name = "US Dollar"
    code = "USD"
    symbol = "$"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Test Income Category"
    type = "income"
    builtin = False
    user = factory.SubFactory("users.factories.UserFactory")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"test tag {n}")
    user = factory.SubFactory("users.factories.UserFactory")

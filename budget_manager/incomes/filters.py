import django_filters
from budget_manager_app.consts import PAYMENT_METHOD_CHOICES
from budget_manager_app.styles import CLASSES
from django import forms
from helper_models.models import Currency, Tag
from incomes.models import Income


class IncomeFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="exact",
        widget=forms.DateInput(attrs={"type": "date", "class": CLASSES}),
    )
    payment_method = django_filters.ChoiceFilter(
        field_name="payment_method",
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={"class": CLASSES}),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": CLASSES}),
    )
    currency = django_filters.ModelChoiceFilter(
        field_name="currency",
        queryset=Currency.objects.all(),
        widget=forms.Select(attrs={"class": CLASSES}),
    )

    class Meta:
        model = Income
        fields = ("date", "payment_method", "tags", "currency")

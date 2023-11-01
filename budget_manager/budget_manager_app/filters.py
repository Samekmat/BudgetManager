import django_filters
from django import forms
from incomes.models import Income
from budget_manager_app.styles import CLASSES
from budget_manager_app.models import PAYMENT_METHOD_CHOICES, Tag, Currency


class IncomeFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='exact',
        widget=forms.DateInput(attrs={"type": "date", 'class': CLASSES})
    )
    payment_method = django_filters.ChoiceFilter(
        field_name='payment_method',
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': CLASSES})
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': CLASSES})
    )
    currency = django_filters.ModelChoiceFilter(
        field_name='currency',
        queryset=Currency.objects.all(),
        widget=forms.Select(attrs={'class': CLASSES})
    )

    class Meta:
        model = Income
        fields = ('date', 'payment_method', 'tags', 'currency')

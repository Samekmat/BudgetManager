import django_filters
from django import forms
from incomes.models import Income
from expenses.models import Expense
from budget_manager_app.styles import CLASSES
from budget_manager_app.choices import PAYMENT_METHOD_CHOICES, CATEGORY_TYPES
from helper_models.models import Tag, Currency, Category


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


class ExpenseFilter(django_filters.FilterSet):
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
        model = Expense
        fields = ('date', 'payment_method', 'tags', 'currency')


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': CLASSES})

    )
    type = django_filters.ChoiceFilter(
        field_name='type',
        choices=CATEGORY_TYPES ,
        widget=forms.Select(attrs={'class': CLASSES})
    )

    class Meta:
        model = Category
        fields = ('name', 'type')


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': CLASSES})
    )

    class Meta:
        model = Tag
        fields = ('name', )


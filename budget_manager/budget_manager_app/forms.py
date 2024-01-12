from budget_manager_app.models import Budget
from budget_manager_app.styles import CLASSES
from django import forms

from expenses.models import Expense
from helper_models.models import Currency
from incomes.models import Income


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ("user", "incomes", "expenses")
        fields = ("name", "currency", "shared_with", "incomes", "expenses", "goals")
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
            "user": forms.Select(attrs={"class": CLASSES}),
            "shared_with": forms.SelectMultiple(attrs={"class": CLASSES}),
            "incomes": forms.SelectMultiple(attrs={"class": CLASSES}),
            "expenses": forms.SelectMultiple(attrs={"class": CLASSES}),
            "goals": forms.SelectMultiple(attrs={"class": CLASSES}),
            "currency": forms.Select(attrs={"class": CLASSES}),
        }


class IncomeExpenseSelectForm(forms.Form):
    incomes = forms.ModelMultipleChoiceField(
        queryset=Income.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    expenses = forms.ModelMultipleChoiceField(
        queryset=Expense.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class CurrencyBaseForm(forms.Form):
    base_currency = forms.ModelChoiceField(
        label="Base Currency",
        queryset=Currency.objects.all(),
        empty_label=None,
        to_field_name="code",
    )


class ChartForm(forms.Form):
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": CLASSES, "type": "date"}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": CLASSES, "type": "date"}))
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": CLASSES}),
    )

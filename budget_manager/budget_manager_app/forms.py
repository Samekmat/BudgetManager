from django import forms

from budget_manager_app.styles import CLASSES

from budget_manager_app.models import Budget, SavingGoal

from expenses.models import Expense
from incomes.models import Income

from helper_models.models import Currency


class SavingGoalForm(forms.ModelForm):
    amount_to_add = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    amount_to_subtract = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = SavingGoal
        fields = ("name", "amount", "goal", "currency",)
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
            "amount": forms.NumberInput(attrs={"class": CLASSES}),
            "goal": forms.NumberInput(attrs={"class": CLASSES}),
            "currency": forms.Select(attrs={"class": CLASSES}),
        }


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
        label='Base Currency',
        queryset=Currency.objects.all(),
        empty_label=None,
        to_field_name='code')


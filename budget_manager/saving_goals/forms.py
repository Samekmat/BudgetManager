from budget_manager_app.styles import CLASSES
from django import forms
from saving_goals.models import SavingGoal


class SavingGoalForm(forms.ModelForm):
    amount_to_add = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    amount_to_subtract = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = SavingGoal
        fields = (
            "name",
            "amount",
            "goal",
            "currency",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
            "amount": forms.NumberInput(attrs={"class": CLASSES}),
            "goal": forms.NumberInput(attrs={"class": CLASSES}),
            "currency": forms.Select(attrs={"class": CLASSES}),
        }

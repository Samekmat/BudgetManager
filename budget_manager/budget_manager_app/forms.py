from budget_manager_app.models import Category, Tag, SavingGoal, CATEGORY_TYPES
from django import forms

from budget_manager_app.styles import CLASSES


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'type')
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
            "description": forms.TextInput(attrs={"class": CLASSES}),
            "type": forms.Select(attrs={"class": CLASSES}, choices=CATEGORY_TYPES),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', )
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
        }


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
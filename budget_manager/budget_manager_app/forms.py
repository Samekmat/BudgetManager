from budget_manager_app.models import Category, Tag
from django import forms

from budget_manager_app.styles import CLASSES


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'is_income')
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
            "description": forms.TextInput(attrs={"class": CLASSES}),
            "is_income": forms.Select(attrs={"class": CLASSES}, choices=((True, 'Yes'), (False, 'No'))),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', )
        widgets = {
            "name": forms.TextInput(attrs={"class": CLASSES}),
        }

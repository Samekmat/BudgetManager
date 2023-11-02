from django import forms

from helper_models.models import Category, Tag

from budget_manager_app.choices import CATEGORY_TYPES
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

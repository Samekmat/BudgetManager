from budget_manager_app.styles import CLASSES
from django import forms
from expenses.models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": CLASSES}),
            "amount": forms.TextInput(attrs={"class": CLASSES, "placeholder": "Enter amount"}),
            "category": forms.Select(attrs={"class": CLASSES}),
            "user": forms.Select(attrs={"class": CLASSES}),
            "payment_method": forms.Select(attrs={"class": CLASSES}),
            "currency": forms.Select(attrs={"class": CLASSES}),
            "tags": forms.SelectMultiple(attrs={"class": CLASSES}),
            "notes": forms.Textarea(attrs={"class": CLASSES, "rows": "4"}),
            "image": forms.ClearableFileInput(attrs={"class": CLASSES}),
        }

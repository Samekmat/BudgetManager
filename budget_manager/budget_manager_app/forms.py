from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from budget_manager_app.styles import CLASSES

from budget_manager_app.models import Income, Expense


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].label_tag(attrs={'class': "text-gray-900 dark:text-white"}) TODO add class
        self.fields['username'].widget.attrs['class'] = CLASSES
        self.fields['email'].widget.attrs['class'] = CLASSES
        self.fields['password1'].widget.attrs['class'] = CLASSES
        self.fields['password2'].widget.attrs['class'] = CLASSES

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = CLASSES
        self.fields['password'].widget.attrs['class'] = CLASSES


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': CLASSES}),
            'amount': forms.TextInput(attrs={'class': CLASSES, 'placeholder': 'Enter amount'}),
            'category': forms.Select(attrs={'class': CLASSES}),
            'user': forms.Select(attrs={'class': CLASSES}),
            'payment_method': forms.Select(attrs={'class': CLASSES}),
            'currency': forms.Select(attrs={'class': CLASSES}),
            'tags': forms.SelectMultiple(attrs={'class': CLASSES}),
            'notes': forms.Textarea(attrs={'class': CLASSES, 'rows': '4'}),
            'image': forms.ClearableFileInput(attrs={'class': CLASSES}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['amount'].widget.attrs['class'] = CLASSES
    #     self.fields['date'].widget.attrs['class'] = CLASSES
    #     self.fields['user'].widget.attrs['class'] = CLASSES
    #     self.fields['category'].widget.attrs['class'] = CLASSES
    #     self.fields['payment_method'].widget.attrs['class'] = CLASSES
    #     self.fields['currency'].widget.attrs['class'] = CLASSES
    #     self.fields['tags'].widget.attrs['class'] = CLASSES
    #     self.fields['image'].widget.attrs['class'] = CLASSES
    #     self.fields['notes'].widget.attrs['class'] = CLASSES


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': CLASSES}),
            'amount': forms.TextInput(attrs={'class': CLASSES, 'placeholder': 'Enter amount'}),
            'category': forms.Select(attrs={'class': CLASSES}),
            'user': forms.Select(attrs={'class': CLASSES}),
            'payment_method': forms.Select(attrs={'class': CLASSES}),
            'currency': forms.Select(attrs={'class': CLASSES}),
            'tags': forms.SelectMultiple(attrs={'class': CLASSES}),
            'notes': forms.Textarea(attrs={'class': CLASSES, 'rows': '4'}),
            'image': forms.ClearableFileInput(attrs={'class': CLASSES}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['amount'].widget.attrs['class'] = CLASSES
    #     self.fields['date'].widget.attrs['class'] = CLASSES
    #     self.fields['user'].widget.attrs['class'] = CLASSES
    #     self.fields['category'].widget.attrs['class'] = CLASSES
    #     self.fields['payment_method'].widget.attrs['class'] = CLASSES
    #     self.fields['currency'].widget.attrs['class'] = CLASSES
    #     self.fields['tags'].widget.attrs['class'] = CLASSES
    #     self.fields['image'].widget.attrs['class'] = CLASSES
    #     self.fields['notes'].widget.attrs['class'] = CLASSES

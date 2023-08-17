from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from budget_manager_app.styles import CLASSES, REMEMBER_ME


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
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = CLASSES
        self.fields['password'].widget.attrs['class'] = CLASSES
        self.fields['remember_me'].widget.attrs['class'] = REMEMBER_ME

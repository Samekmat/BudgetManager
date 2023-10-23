from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from budget_manager_app.styles import CLASSES


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].label_tag(attrs={'class': "text-gray-900 dark:text-white"}) TODO add class
        self.fields["username"].widget.attrs["class"] = CLASSES
        self.fields["email"].widget.attrs["class"] = CLASSES
        self.fields["password1"].widget.attrs["class"] = CLASSES
        self.fields["password2"].widget.attrs["class"] = CLASSES

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = CLASSES
        self.fields["password"].widget.attrs["class"] = CLASSES

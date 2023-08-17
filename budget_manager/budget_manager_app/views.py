from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from budget_manager_app.forms import RegisterForm, LoginForm


def index(request):
    return render(request, 'index.html')


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import RegisterForm, LoginForm


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def get_next_page(self):
        next_page = self.request.POST.get('next', self.request.GET.get('next', ''))
        return next_page if next_page else self.next_page

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import LoginForm, RegisterForm


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(self.request, "Registration successful. You are now logged in.")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    # def form_valid(self, form):
    #     user = authenticate(request=self.request, username=form.cleaned_data['username'], password=form.cleaned_data["password"])
    #     if user is not None:
    #         login(self.request, user)
    #     messages.success(self.request, "Login successful. Welcome back!")
    #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         user = authenticate(request=request, username=form.cleaned_data['username'],
    #                             password=form.cleaned_data["password"])
    #         if user is not None:
    #             login(request, user)
    #         messages.success(request, "Login successful. Welcome back!")
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("users:login")

    def get_next_page(self):
        next_page = self.request.POST.get("next", self.request.GET.get("next", ""))
        return next_page if next_page else self.next_page

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

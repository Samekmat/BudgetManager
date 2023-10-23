from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, UpdateView
from budget_manager_app.forms import RegisterForm, LoginForm, IncomeForm, ExpenseForm

from budget_manager_app.models import Income, CategoryIncome, Currency, Expense


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


class IncomeListView(ListView):
    model = Income
    template_name = 'crud/incomes.html'
    context_object_name = 'incomes'

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['form'] = IncomeForm()
        return super().get_context_data(**kwargs)


class IncomeCreateView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'crud/incomes.html'
    success_url = reverse_lazy('incomes')

    def form_valid(self, form):
        messages.success(self.request, 'Income created successfully.')
        return super().form_valid(form)


class IncomeUpdateView(UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'crud/edit_income.html'
    success_url = reverse_lazy('incomes')

    def form_valid(self, form):
        messages.success(self.request, 'Income updated successfully.')
        return super().form_valid(form)


class ExpenseListView(ListView):
    model = Expense
    template_name = 'crud/expenses.html'
    context_object_name = 'expenses'

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['form'] = IncomeForm()
        return super().get_context_data(**kwargs)


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'crud/expenses.html'
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        messages.success(self.request, 'Expense created successfully.')
        return super().form_valid(form)


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'crud/edit_expense.html'
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully.')
        return super().form_valid(form)

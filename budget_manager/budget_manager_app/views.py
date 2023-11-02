from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from budget_manager_app.forms import BudgetForm, SavingGoalForm
from budget_manager_app.models import Budget, SavingGoal


from incomes.models import Income
from expenses.models import Expense

import freecurrencyapi

from django.conf import settings


def index(request):
    return render(request, "index.html")


class SavingGoalListView(ListView):
    model = SavingGoal
    template_name = 'saving_goals/goals.html'
    context_object_name = 'goals'

    def post(self, request, *args, **kwargs):
        goal_id = request.POST.get('goal_id')
        goal = SavingGoal.objects.get(id=goal_id)

        if 'amount_to_add' in request.POST:
            amount_to_add = Decimal(request.POST.get('amount_to_add'))
            if amount_to_add > Decimal(0):
                goal.amount += amount_to_add
                messages.success(request, f"Added {amount_to_add}{goal.currency.symbol} to the goal.")
            else:
                messages.error(request, "Invalid amount to add.")
        elif 'amount_to_subtract' in request.POST:
            amount_to_subtract = Decimal(request.POST.get('amount_to_subtract'))
            if goal.amount - amount_to_subtract >= Decimal(0):
                goal.amount -= amount_to_subtract
                messages.success(request, f"Subtracted {amount_to_subtract}{goal.currency.symbol}  from the goal.")
            else:
                messages.error(request, "Invalid amount to subtract")

        goal.save()
        return redirect('goals')


class SavingGoalCreateView(CreateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('goals')

    def form_valid(self, form):
        messages.success(self.request, 'Saving goal created successfully.')
        return super().form_valid(form)


class SavingGoalUpdateView(UpdateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('goals')

    def form_valid(self, form):
        messages.success(self.request, 'Saving goal updated successfully.')
        return super().form_valid(form)


class SavingGoalDeleteView(DeleteView):
    model = SavingGoal
    template_name = 'saving_goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goals')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Saving goal deleted successfully.')
        return super().delete(request, *args, **kwargs)


class DashboardListView(ListView):
    template_name = 'dashboard.html'
    context_object_name = 'dashboard'

    def get_queryset(self):
        income_query = Income.objects.order_by('-date')[:2]
        expense_query = Expense.objects.order_by('-date')[:2]

        recent_transactions = list(income_query) + list(expense_query)
        recent_transactions.sort(key=lambda x: x.date, reverse=True)

        exchange_rates = self.get_exchange_rates()

        return recent_transactions, exchange_rates

    def get_exchange_rates(self):
        api_key = settings.FREE_CURRENCY_API_KEY
        client = freecurrencyapi.Client(api_key)
        return client.latest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_transactions, exchange_rates = self.get_queryset()

        context['dashboard'] = recent_transactions
        context['exchange_rates'] = exchange_rates

        return context


class BudgetListView(ListView):
    model = Budget
    template_name = 'budgets/budgets.html'
    context_object_name = 'budgets'


class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets')

    def form_valid(self, form):
        messages.success(self.request, 'Budget created successfully.')
        return super().form_valid(form)


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets')

    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully.')
        return super().form_valid(form)


class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budgets')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Budget deleted successfully.')
        return super().delete(request, *args, **kwargs)

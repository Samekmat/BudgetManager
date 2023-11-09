from decimal import Decimal

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, DetailView, FormView
from budget_manager_app.forms import BudgetForm, SavingGoalForm, IncomeExpenseSelectForm
from budget_manager_app.models import Budget, SavingGoal

from incomes.models import Income
from expenses.models import Expense

import freecurrencyapi

from plotly.offline import plot
import plotly.graph_objs as go

import pandas as pd
import plotly.express as px

from budget_manager_app.forms import CurrencyBaseForm


def index(request):
    return render(request, "index.html")


class SavingGoalListView(LoginRequiredMixin, ListView):
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
        return redirect('budgets:goals')

    def get_queryset(self):
        user_goals = SavingGoal.objects.filter(user=self.request.user)
        return user_goals


class SavingGoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('budgets:goals')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Saving goal created successfully.')
        return super().form_valid(form)


class SavingGoalUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('budgets:goals')

    def form_valid(self, form):
        messages.success(self.request, 'Saving goal updated successfully.')
        return super().form_valid(form)

    def get_queryset(self):
        user_goals = SavingGoal.objects.filter(user=self.request.user)
        return user_goals


class SavingGoalDetailView(LoginRequiredMixin, DetailView):
    model = SavingGoal
    template_name = 'saving_goals/goal_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            return HttpResponseForbidden("You don't have permission to access this goal.")
        return obj


class SavingGoalDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingGoal
    template_name = 'saving_goals/goal_confirm_delete.html'
    success_url = reverse_lazy('budgets:goals')

    def delete(self, request, *args, **kwargs):
        goal = self.get_object()
        if goal.user == self.request.user:
            messages.success(self.request, 'Saving goal deleted successfully.')
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to delete this goal.")


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    context_object_name = 'dashboard'

    def get_exchange_rates(self, base_currency):
        api_key = settings.FREE_CURRENCY_API_KEY
        client = freecurrencyapi.Client(api_key)
        return client.latest(base_currency=base_currency)

    def get_context_data(self, **kwargs):
        user = self.request.user

        income_query = Income.objects.filter(user=user).order_by('-date')[:2]
        expense_query = Expense.objects.filter(user=user).order_by('-date')[:2]

        recent_transactions = list(income_query) + list(expense_query)
        recent_transactions.sort(key=lambda x: x.date, reverse=True)

        currency_form = CurrencyBaseForm()
        base_currency = self.request.GET.get('base_currency', 'USD')

        exchange_rates = self.get_exchange_rates(base_currency)

        context = super().get_context_data(**kwargs)

        context['dashboard'] = recent_transactions
        context['exchange_rates'] = exchange_rates
        context['base_currency'] = base_currency
        context['currency_form'] = currency_form
        return context


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/budgets.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        user_budgets = Budget.objects.filter(user=self.request.user)
        return user_budgets


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets:budgets')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Budget created successfully.')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        logged_in_user = self.request.user
        form.fields['shared_with'].queryset = User.objects.exclude(id=logged_in_user.id)
        return form


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets:budgets')

    def get_queryset(self):
        user_budgets = Budget.objects.filter(user=self.request.user)
        return user_budgets

    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully.')
        return super().form_valid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budgets:budgets')

    def delete(self, request, *args, **kwargs):
        budget = self.get_object()
        if budget.user == self.request.user:
            messages.success(self.request, 'Budget deleted successfully.')
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to delete this budget.")


class ChartView(LoginRequiredMixin, View):
    template_name = 'budgets/charts.html'

    def get_context_data(self, budget):
        income_categories = budget.incomes.values('category__name').annotate(total=Sum('amount'))
        expense_categories = budget.expenses.values('category__name').annotate(total=Sum('amount'))
        total_balance = budget.calculate_balance
        incomes = budget.incomes.values('date').annotate(total=Sum('amount'))
        expenses = budget.expenses.values('date').annotate(total=Sum('amount'))

        return {
            'income_categories': income_categories,
            'expense_categories': expense_categories,
            'total_balance': total_balance,
            'incomes': incomes,
            'expenses': expenses,
        }

    def generate_bar_chart(self, budget):
        context = self.get_context_data(budget)

        # Calculate the total income and total expenses
        total_incomes = sum(item['total'] for item in context['incomes'])
        total_expenses = sum(item['total'] for item in context['expenses'])

        # Calculate the percentages
        income_percentage = (total_incomes / (total_incomes + total_expenses)) * 100
        expense_percentage = (total_expenses / (total_incomes + total_expenses)) * 100

        fig = go.Figure()

        # Create two bars for "Incomes" and "Expenses" and display percentages on the bars
        fig.add_trace(go.Bar(
            x=["Incomes"],
            y=[total_incomes],
            text=[f'{income_percentage:.2f}%'],  # Format the percentage
            name='Incomes',
        ))

        fig.add_trace(go.Bar(
            x=["Expenses"],
            y=[total_expenses],
            text=[f'{expense_percentage:.2f}%'],  # Format the percentage
            name='Expenses',
        ))

        fig.update_layout(
            title='Total Incomes vs Total Expenses',
            xaxis_title='',
            yaxis_title='Amount',
            barmode='group',  # Use 'group' for grouped bars
        )

        return plot(fig, output_type='div')

    def generate_pie_chart(self, budget):
        context = self.get_context_data(budget)

        labels = ["Incomes", "Expenses"]
        values = [sum(item['total'] for item in context['incomes']), sum(item['total'] for item in context['expenses'])]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(
            height=450,
            width=450
        )
        return plot(fig, output_type='div')

    def generate_budget_chart(self, budget):
        total_balance = budget.calculate_balance

        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=total_balance,
            title="Total Balance",
            number={'prefix': budget.currency.symbol},
        ))

        return plot(fig, output_type='div')

    def generate_income_category_pie_chart(self, budget):
        context = self.get_context_data(budget)

        # Extract category names and their total incomes
        labels = [item['category__name'] for item in context['income_categories']]
        values = [item['total'] for item in context['income_categories']]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(title='Income Categories')

        return plot(fig, output_type='div')

    def generate_expense_category_pie_chart(self, budget):
        context = self.get_context_data(budget)

        # Extract category names and their total expenses
        labels = [item['category__name'] for item in context['expense_categories']]
        values = [item['total'] for item in context['expense_categories']]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(title='Expense Categories')

        return plot(fig, output_type='div')

    def generate_line_chart(self, budget):
        # Collect and process income data by date
        income_data = budget.incomes.values('date').annotate(total=Sum('amount')).order_by('date')
        income_dates = [item['date'] for item in income_data]
        income_totals = [item['total'] for item in income_data]

        # Collect and process expense data by date
        expense_data = budget.expenses.values('date').annotate(total=Sum('amount')).order_by('date')
        expense_dates = [item['date'] for item in expense_data]
        expense_totals = [-item['total'] for item in expense_data]

        # Create a list of all unique dates (union of income and expense dates)
        all_dates = sorted(set(income_dates + expense_dates))

        # Calculate the daily differences (profit/loss)
        daily_differences = []
        for date in all_dates:
            income = income_totals[income_dates.index(date)] if date in income_dates else 0
            expense = expense_totals[expense_dates.index(date)] if date in expense_dates else 0
            daily_differences.append(income + expense)

        # Create a Plotly figure
        fig = go.Figure()

        # Add lines for income, expenses, and difference with markers
        fig.add_trace(go.Scatter(x=income_dates, y=income_totals, mode='lines+markers', name='Income'))
        fig.add_trace(go.Scatter(x=expense_dates, y=expense_totals, mode='lines+markers', name='Expenses'))
        fig.add_trace(go.Scatter(x=all_dates, y=daily_differences, mode='lines+markers', name='Difference'))

        # Update the layout
        fig.update_layout(
            title="Budget Overview",
            xaxis_title="Date",
            yaxis_title="Amount",
        )

        chart_div = plot(fig, output_type='div', include_plotlyjs=False)

        return chart_div

    def get(self, request, budget_id):
        user = self.request.user
        budget = Budget.objects.get(pk=budget_id, user=user)

        income_chart = self.generate_pie_chart(budget)
        budget_chart = self.generate_budget_chart(budget)
        income_category_chart = self.generate_income_category_pie_chart(budget)
        expense_category_chart = self.generate_expense_category_pie_chart(budget)
        line_chart = self.generate_line_chart(budget)
        bar_chart = self.generate_bar_chart(budget)

        return render(request, self.template_name, {
            'income_chart': income_chart,
            'budget_chart': budget_chart,
            'income_category_chart': income_category_chart,
            'expense_category_chart': expense_category_chart,
            'line_chart': line_chart,
            'bar_chart': bar_chart
        })


class AddIncomeExpenseView(View):
    template_name = 'budgets/add_income_expense.html'

    def get(self, request, budget_id):
        budget = Budget.objects.get(pk=budget_id)
        form = IncomeExpenseSelectForm()

        # Filter incomes and expenses by the specified currency
        selected_currency = budget.currency
        form.fields['incomes'].queryset = Income.objects.filter(currency=selected_currency)
        form.fields['expenses'].queryset = Expense.objects.filter(currency=selected_currency)

        return render(request, self.template_name, {'form': form, 'budget': budget})

    def post(self, request, budget_id):
        budget = Budget.objects.get(pk=budget_id)
        form = IncomeExpenseSelectForm(request.POST)

        if form.is_valid():
            selected_incomes = form.cleaned_data['incomes']
            selected_expenses = form.cleaned_data['expenses']

            for income in selected_incomes:
                budget.incomes.add(income)

            for expense in selected_expenses:
                budget.expenses.add(expense)

            return redirect('budgets:budgets')  # Redirect to the budget list view

        return render(request, self.template_name, {'form': form, 'budget': budget})

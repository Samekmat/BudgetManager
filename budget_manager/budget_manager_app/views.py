from decimal import Decimal

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, DetailView
from budget_manager_app.forms import BudgetForm, SavingGoalForm
from budget_manager_app.models import Budget, SavingGoal

from incomes.models import Income
from expenses.models import Expense

import freecurrencyapi

from plotly.offline import plot
import plotly.graph_objs as go


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
        return redirect('budgets:goals')


class SavingGoalCreateView(CreateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('budgets:goals')

    def form_valid(self, form):
        messages.success(self.request, 'Saving goal created successfully.')
        return super().form_valid(form)


class SavingGoalUpdateView(UpdateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('budgets:goals')

    def form_valid(self, form):
        messages.success(self.request, 'Saving goal updated successfully.')
        return super().form_valid(form)


class SavingGoalDetailView(DetailView):
    model = SavingGoal
    template_name = 'saving_goals/goal_detail.html'


class SavingGoalDeleteView(DeleteView):
    model = SavingGoal
    template_name = 'saving_goals/goal_confirm_delete.html'
    success_url = reverse_lazy('budgets:goals')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Saving goal deleted successfully.')
        return super().delete(request, *args, **kwargs)


class DashboardListView(TemplateView):
    template_name = 'dashboard.html'
    context_object_name = 'dashboard'



    def get_exchange_rates(self):
        api_key = settings.FREE_CURRENCY_API_KEY
        client = freecurrencyapi.Client(api_key)
        return client.latest()

    def get_context_data(self, **kwargs):
        income_query = Income.objects.order_by('-date')[:2]
        expense_query = Expense.objects.order_by('-date')[:2]

        recent_transactions = list(income_query) + list(expense_query)
        recent_transactions.sort(key=lambda x: x.date, reverse=True)

        exchange_rates = self.get_exchange_rates()

        context = super().get_context_data(**kwargs)

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
    success_url = reverse_lazy('budgets:budgets')

    def form_valid(self, form):
        messages.success(self.request, 'Budget created successfully.')
        return super().form_valid(form)


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets:budgets')

    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully.')
        return super().form_valid(form)


class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budgets:budgets')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Budget deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ChartView(View):
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

    def generate_pie_chart(self, budget):
        context = self.get_context_data(budget)

        labels = ["Incomes", "Expenses"]
        values = [sum(item['total'] for item in context['incomes']), sum(item['total'] for item in context['expenses'])]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        return plot(fig, output_type='div')

    def generate_budget_chart(self, budget):
        context = self.get_context_data(budget)

        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=context['total_balance'],
            title="Total Balance",
            number={'prefix': "$"},
        ))

        return plot(fig, output_type='div')

    def generate_bar_chart(self, budget):
        context = self.get_context_data(budget)

        fig = go.Figure()

        # Create two bars for "Incomes" and "Expenses"
        fig.add_trace(go.Bar(
            x=["Incomes"],
            y=[sum(item['total'] for item in context['incomes'])],
            name='Incomes',
        ))

        fig.add_trace(go.Bar(
            x=["Expenses"],
            y=[sum(item['total'] for item in context['expenses'])],
            name='Expenses',
        ))

        fig.update_layout(
            title='Total Incomes vs Total Expenses',
            xaxis_title='',
            yaxis_title='Amount',
            barmode='group',  # Use 'group' for grouped bars
        )

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
        expense_totals = [item['total'] for item in expense_data]

        # Create a list of all unique dates (union of income and expense dates)
        all_dates = sorted(set(income_dates + expense_dates))

        # Calculate the daily differences (profit/loss)
        daily_differences = []
        for date in all_dates:
            income = income_totals[income_dates.index(date)] if date in income_dates else 0
            expense = expense_totals[expense_dates.index(date)] if date in expense_dates else 0
            daily_differences.append(income - expense)

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
        budget = Budget.objects.get(pk=budget_id)

        income_chart = self.generate_pie_chart(budget)
        budget_chart = self.generate_budget_chart(budget)
        bar_chart = self.generate_bar_chart(budget)

        income_category_chart = self.generate_income_category_pie_chart(budget)
        expense_category_chart = self.generate_expense_category_pie_chart(budget)
        line_chart = self.generate_line_chart(budget)

        return render(request, self.template_name, {
            'income_chart': income_chart,
            'budget_chart': budget_chart,
            'bar_chart': bar_chart,
            'income_category_chart': income_category_chart,
            'expense_category_chart': expense_category_chart,
            'line_chart': line_chart
        })

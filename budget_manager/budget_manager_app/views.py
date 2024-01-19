import re

import freecurrencyapi
import pytesseract
from budget_manager_app.charts.generate_budget_charts import ChartsBudgetsGenerator
from budget_manager_app.charts.generate_dashboard_charts import ChartsDashboardGenerator
from budget_manager_app.forms import (
    BudgetForm,
    ChartForm,
    CurrencyBaseForm,
    ImageUploadForm,
    IncomeExpenseSelectForm,
)
from budget_manager_app.models import Budget
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from expenses.models import Expense
from incomes.models import Income
from PIL import Image


def index(request):
    return render(request, "index.html")


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = "budgets/budgets.html"
    context_object_name = "budgets"

    def get_queryset(self):
        user = self.request.user
        user_budgets = Budget.objects.filter(Q(user=user) | Q(shared_with=user)).distinct()
        return user_budgets


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budgets:budgets")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Budget created successfully.")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        logged_in_user = self.request.user
        form.fields["shared_with"].queryset = User.objects.exclude(id=logged_in_user.id)
        return form


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budgets:budgets")

    def get_queryset(self):
        user_budgets = Budget.objects.filter(user=self.request.user)
        return user_budgets

    def form_valid(self, form):
        messages.success(self.request, "Budget updated successfully.")
        return super().form_valid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = "budgets/budget_confirm_delete.html"
    success_url = reverse_lazy("budgets:budgets")

    def delete(self, request, *args, **kwargs):
        budget = self.get_object()
        if budget.user == self.request.user:
            messages.success(self.request, "Budget deleted successfully.")
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to delete this budget.")


class ChartView(LoginRequiredMixin, View):
    template_name = "budgets/charts.html"

    def get_context_data(self, budget):
        income_categories = budget.incomes.values("category__name").annotate(total=Sum("amount"))
        expense_categories = budget.expenses.values("category__name").annotate(total=Sum("amount"))
        total_balance = budget.calculate_balance
        incomes = budget.incomes.values("date").annotate(total=Sum("amount"))
        expenses = budget.expenses.values("date").annotate(total=Sum("amount"))

        return {
            "budget": budget,
            "income_categories": income_categories,
            "expense_categories": expense_categories,
            "total_balance": total_balance,
            "incomes": incomes,
            "expenses": expenses,
        }

    def get(self, request, budget_id):
        user = self.request.user
        budget = Budget.objects.get(pk=budget_id, user=user)

        context = self.get_context_data(budget)

        income_chart = ChartsBudgetsGenerator.generate_pie_chart(context)
        budget_chart = ChartsBudgetsGenerator.generate_budget_chart(context)
        income_category_chart = ChartsBudgetsGenerator.generate_income_category_pie_chart(context)
        expense_category_chart = ChartsBudgetsGenerator.generate_expense_category_pie_chart(context)
        line_chart = ChartsBudgetsGenerator.generate_line_chart(context)
        bar_chart = ChartsBudgetsGenerator.generate_bar_chart(context)

        return render(
            request,
            self.template_name,
            {
                "income_chart": income_chart,
                "budget_chart": budget_chart,
                "income_category_chart": income_category_chart,
                "expense_category_chart": expense_category_chart,
                "line_chart": line_chart,
                "bar_chart": bar_chart,
            },
        )


class AddIncomeExpenseView(View):
    template_name = "budgets/add_income_expense.html"

    def get(self, request, budget_id):
        budget = Budget.objects.get(pk=budget_id)

        if request.user == budget.user or request.user in budget.shared_with.all():
            form = IncomeExpenseSelectForm()

            selected_currency = budget.currency

            all_users = [budget.user] + list(budget.shared_with.all())
            form.fields["incomes"].queryset = Income.objects.filter(currency=selected_currency, user__in=all_users)
            form.fields["expenses"].queryset = Expense.objects.filter(currency=selected_currency, user__in=all_users)

            return render(request, self.template_name, {"form": form, "budget": budget})
        else:
            return HttpResponseForbidden("You do not have permission to access this budget.")

    def post(self, request, budget_id):
        budget = Budget.objects.get(pk=budget_id)
        form = IncomeExpenseSelectForm(request.POST)

        if form.is_valid():
            selected_incomes = form.cleaned_data["incomes"]
            selected_expenses = form.cleaned_data["expenses"]

            for income in selected_incomes:
                budget.incomes.add(income)

            for expense in selected_expenses:
                budget.expenses.add(expense)

            return redirect("budgets:budgets")  # Redirect to the budget list view

        return render(request, self.template_name, {"form": form, "budget": budget})


class DashboardView(View):
    template_name = "budgets/dashboard.html"

    def get(self, request):
        form = ChartForm(request.GET or None)
        currency_form = CurrencyBaseForm()
        user = request.user

        base_currency = self.request.GET.get("base_currency", "USD")
        exchange_rates = self.get_exchange_rates(base_currency)

        income_query = Income.objects.filter(user=user).order_by("-date")[:2]
        expense_query = Expense.objects.filter(user=user).order_by("-date")[:2]

        recent_transactions = list(income_query) + list(expense_query)
        recent_transactions.sort(key=lambda x: x.date, reverse=True)

        expense_comparison = Expense.compare_expenses(request)

        if currency_form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "currency_form": currency_form,
                    "exchange_rates": exchange_rates,
                },
            )

        if request.GET and form.is_valid():
            expenses = Expense.objects.filter(user=user)
            incomes = Income.objects.filter(user=user)

            line_chart = ChartsDashboardGenerator.generate_line_chart(form, expenses, incomes)
            income_pie_chart = ChartsDashboardGenerator.generate_pie_chart(
                Income,
                form.cleaned_data.get("date_from"),
                form.cleaned_data.get("date_to"),
                form.cleaned_data.get("currency"),
                "Income Categories",
            )
            expense_pie_chart = ChartsDashboardGenerator.generate_pie_chart(
                Expense,
                form.cleaned_data.get("date_from"),
                form.cleaned_data.get("date_to"),
                form.cleaned_data.get("currency"),
                "Expense Categories",
            )
            percentage_bar_chart = ChartsDashboardGenerator.generate_percentage_bar_chart(form, expenses, incomes)

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "line_chart": line_chart,
                    "income_pie_chart": income_pie_chart,
                    "expense_pie_chart": expense_pie_chart,
                    "percentage_bar_chart": percentage_bar_chart,
                    "recent_transactions": recent_transactions,
                    "base_currency": base_currency,
                    "currency_form": currency_form,
                    "exchange_rates": exchange_rates,
                },
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "currency_form": currency_form,
                "exchange_rates": exchange_rates,
                "base_currency": base_currency,
                "recent_transactions": recent_transactions,
                "expense_comparison_results": expense_comparison,
            },
        )

    def get_exchange_rates(self, base_currency):
        api_key = settings.FREE_CURRENCY_API_KEY
        client = freecurrencyapi.Client(api_key)
        return client.latest(base_currency=base_currency)


class ProcessImageView(FormView):
    template_name = "process-image.html"
    form_class = ImageUploadForm
    success_url = reverse_lazy("process_image")

    def form_valid(self, form):
        image = form.cleaned_data["image"]

        text_result = self.process_image(image)

        amount_pattern = re.compile(r"TOTAL\s+\$([\d.]+)", re.IGNORECASE)
        date_pattern = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")
        currency_pattern = re.compile(r"(\$|USD|EUR|PLN|€|zł)")
        payment_method_pattern = re.compile(r"(Bank|Card|Cash)", re.IGNORECASE)

        # Extract information using regex
        amount_match = amount_pattern.search(text_result)
        date_match = date_pattern.search(text_result)
        currency_match = currency_pattern.search(text_result)
        payment_method_match = payment_method_pattern.search(text_result)

        extracted_info = {
            "amount": amount_match.group(1) if amount_match else None,
            "date": date_match.group() if date_match else None,
            "currency": currency_match.group() if currency_match else None,
            "payment_method": payment_method_match.group() if payment_method_match else None,
        }

        return self.render_to_response(self.get_context_data(extracted_info=extracted_info, text_result=text_result))

    def process_image(self, image):
        # Convert image to grayscale
        image = Image.open(image).convert("L")

        # Use pytesseract to extract text
        text_result = pytesseract.image_to_string(image)

        return text_result

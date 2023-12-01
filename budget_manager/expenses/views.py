from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from expenses.forms import ExpenseForm
from expenses.models import Expense

from budget_manager_app.filters import ExpenseFilter
from budget_manager_app.decorators import keep_parameters

class FilteredPaginationMixin:

    def get_filtered_queryset(self, filter_object):
        return filter_object(self.request.GET, queryset=self.get_queryset()).qs

    def get_paginated_result(self, filter_object):
        filtered_queryset = self.get_filtered_queryset(filter_object)
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            pagination = paginator.page(page)
        except PageNotAnInteger:
            pagination = paginator.page(1)
        except EmptyPage:
            pagination = paginator.page(paginator.num_pages)

        return pagination

@keep_parameters
class ExpenseListView(LoginRequiredMixin, FilteredPaginationMixin, ListView):
    model = Expense
    template_name = "expenses/expenses.html"
    context_object_name = "expenses"
    paginate_by = 5
    ordering = ['-date']

    def get_queryset(self):
        user_expenses = Expense.objects.filter(user=self.request.user).order_by('-date')
        return user_expenses

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ExpenseForm()

        # Apply the ExpenseFilter on the filtered queryset
        filtered_queryset = ExpenseFilter(self.request.GET, queryset=self.get_queryset()).qs

        # Paginate the filtered queryset
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)

        context['filter'] = ExpenseFilter(self.request.GET, queryset=filtered_queryset)
        context['expenses'] = expenses
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expenses.html"
    success_url = reverse_lazy("expenses:expenses")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Expense created successfully.")
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/edit_expense.html"
    success_url = reverse_lazy("expenses:expenses")

    def get_queryset(self):
        user_expenses = Expense.objects.filter(user=self.request.user)
        return user_expenses

    def form_valid(self, form):
        messages.success(self.request, "Expense updated successfully.")
        return super().form_valid(form)

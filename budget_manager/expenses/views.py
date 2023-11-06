from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from expenses.forms import ExpenseForm
from expenses.models import Expense

from budget_manager_app.filters import ExpenseFilter
from budget_manager_app.decorators import keep_parameters


@keep_parameters
class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expenses.html"
    context_object_name = "expenses"
    paginate_by = 5
    ordering = ['-date']

    def get_queryset(self):
        expense_filter = ExpenseFilter(self.request.GET, queryset=super().get_queryset())
        return expense_filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ExpenseForm()
        context['filter'] = ExpenseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expenses.html"
    success_url = reverse_lazy("expenses:expenses")

    def form_valid(self, form):
        messages.success(self.request, "Expense created successfully.")
        return super().form_valid(form)


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/edit_expense.html"
    success_url = reverse_lazy("expenses:expenses")

    def form_valid(self, form):
        messages.success(self.request, "Expense updated successfully.")
        return super().form_valid(form)

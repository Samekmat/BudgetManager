from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from expenses.forms import ExpenseForm
from expenses.models import Expense


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expenses.html"
    context_object_name = "expenses"

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs["form"] = ExpenseForm()
        return super().get_context_data(**kwargs)


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

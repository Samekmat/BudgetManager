from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from incomes.forms import IncomeForm
from incomes.models import Income

from budget_manager_app.filters import IncomeFilter

from budget_manager_app.decorators import keep_parameters


@keep_parameters
class IncomeListView(ListView):
    model = Income
    template_name = "incomes/incomes.html"
    context_object_name = "incomes"
    paginate_by = 5
    ordering = ['-date']

    def get_queryset(self):
        income_filter = IncomeFilter(self.request.GET, queryset=super().get_queryset())
        return income_filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IncomeForm()
        context['filter'] = IncomeFilter(self.request.GET, queryset=self.get_queryset())
        return context


class IncomeCreateView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "incomes/incomes.html"
    success_url = reverse_lazy("incomes:incomes")

    def form_valid(self, form):
        messages.success(self.request, "Income created successfully.")
        return super().form_valid(form)


class IncomeUpdateView(UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "incomes/edit_income.html"
    success_url = reverse_lazy("incomes:incomes")

    def form_valid(self, form):
        messages.success(self.request, "Income updated successfully.")
        return super().form_valid(form)

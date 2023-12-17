from budget_manager_app.decorators import keep_parameters
from budget_manager_app.filters import IncomeFilter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from incomes.forms import IncomeForm
from incomes.models import Income


@keep_parameters
class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = "incomes/incomes.html"
    context_object_name = "incomes"
    paginate_by = 5
    ordering = ["-date"]

    def get_queryset(self):
        user_incomes = Income.objects.filter(user=self.request.user).order_by("-date")
        return user_incomes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IncomeForm()

        # Apply the IncomeFilter on the filtered queryset
        filtered_queryset = IncomeFilter(self.request.GET, queryset=self.get_queryset()).qs

        # Paginate the filtered queryset
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            incomes = paginator.page(page)
        except PageNotAnInteger:
            incomes = paginator.page(1)
        except EmptyPage:
            incomes = paginator.page(paginator.num_pages)

        context["filter"] = IncomeFilter(self.request.GET, queryset=filtered_queryset)
        context["incomes"] = incomes
        return context


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "incomes/incomes.html"
    success_url = reverse_lazy("incomes:incomes")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Income created successfully.")
        return super().form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "incomes/edit_income.html"
    success_url = reverse_lazy("incomes:incomes")

    def get_queryset(self):
        user_incomes = Income.objects.filter(user=self.request.user)
        return user_incomes

    def form_valid(self, form):
        messages.success(self.request, "Income updated successfully.")
        return super().form_valid(form)

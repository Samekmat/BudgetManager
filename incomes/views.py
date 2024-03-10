from datetime import date

import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from xhtml2pdf import pisa

from budget_manager_app.decorators import keep_parameters
from incomes.filters import IncomeFilter
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
        user_incomes = (
            Income.objects.filter(user=self.request.user)
            .order_by("-date")
            .select_related("currency", "category")
            .prefetch_related("tags")
        )
        return user_incomes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IncomeForm()

        filtered_queryset = IncomeFilter(self.request.GET, queryset=self.get_queryset()).qs

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


class ExportIncomesCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        incomes = Income.objects.filter(user=user)
        data = {
            "Amount": [income.amount for income in incomes],
            "Date": [income.date for income in incomes],
            "Category": [income.category.name for income in incomes],
            "Payment Method": [income.payment_method for income in incomes],
            "Currency": [income.currency.symbol for income in incomes],
            "Tags": [", ".join(tag.name for tag in income.tags.all()) for income in incomes],
            "Notes": [income.notes for income in incomes],
        }

        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="income_report_{user}[{date.today()}].csv"'
        response.write(csv_string)
        return response


class ExportIncomesPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        incomes = Income.objects.filter(user=user)
        data = {
            "Amount": [income.amount for income in incomes],
            "Date": [income.date for income in incomes],
            "Category": [income.category.name for income in incomes],
            "Payment Method": [income.payment_method for income in incomes],
            "Currency": [income.currency.symbol for income in incomes],
            "Tags": [", ".join(tag.name for tag in income.tags.all()) for income in incomes],
            "Notes": [income.notes for income in incomes],
        }

        df = pd.DataFrame(data)
        currency_totals = df.groupby("Currency")["Amount"].sum().to_dict()

        # Create a PDF document
        template_path = "incomes/income_pdf_template.html"
        template = get_template(template_path)
        context = {"df": df, "incomes": incomes, "currency_totals": currency_totals}
        html = template.render(context)

        # Create PDF from HTML
        pdf_response = HttpResponse(content_type="application/pdf")
        pdf_response["Content-Disposition"] = f'attachment; filename="income_report_{user}[{date.today()}].pdf"'

        pisa_status = pisa.CreatePDF(html, dest=pdf_response)

        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")

        return pdf_response

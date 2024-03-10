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
from expenses.filters import ExpenseFilter
from expenses.forms import ExpenseForm
from expenses.models import Expense


@keep_parameters
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "expenses/expenses.html"
    context_object_name = "expenses"
    paginate_by = 5
    ordering = ["-date"]

    def get_queryset(self):
        user_expenses = Expense.objects.filter(user=self.request.user).order_by("-date")
        return user_expenses

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ExpenseForm()

        filtered_queryset = ExpenseFilter(self.request.GET, queryset=self.get_queryset()).qs

        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)

        context["filter"] = ExpenseFilter(self.request.GET, queryset=filtered_queryset)
        context["expenses"] = expenses
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


class ExportExpensesCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        expenses = Expense.objects.filter(user=user)
        data = {
            "Amount": [expense.amount for expense in expenses],
            "Date": [expense.date for expense in expenses],
            "Category": [expense.category.name for expense in expenses],
            "Payment Method": [expense.payment_method for expense in expenses],
            "Currency": [expense.currency.symbol for expense in expenses],
            "Tags": [", ".join(tag.name for tag in expense.tags.all()) for expense in expenses],
            "Notes": [expense.notes for expense in expenses],
        }

        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="expense_report_{user}[{date.today()}].csv"'
        response.write(csv_string)
        return response


class ExportExpensesPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        expenses = Expense.objects.filter(user=user).select_related("category", "currency").prefetch_related("tags")
        data = {
            "Amount": [expense.amount for expense in expenses],
            "Date": [expense.date for expense in expenses],
            "Category": [expense.category.name for expense in expenses],
            "Payment Method": [expense.payment_method for expense in expenses],
            "Currency": [expense.currency.symbol for expense in expenses],
            "Tags": [", ".join(tag.name for tag in expense.tags.all()) for expense in expenses],
            "Notes": [expense.notes for expense in expenses],
        }

        df = pd.DataFrame(data)
        currency_totals = df.groupby("Currency")["Amount"].sum().to_dict()

        # Create a PDF document
        template_path = "expenses/expense_pdf_template.html"
        template = get_template(template_path)
        context = {"df": df, "expenses": expenses, "currency_totals": currency_totals}
        html = template.render(context)

        # Create PDF from HTML
        pdf_response = HttpResponse(content_type="application/pdf")
        pdf_response["Content-Disposition"] = f'attachment; filename="expense_report_{user}[{date.today()}].pdf"'

        pisa_status = pisa.CreatePDF(html, dest=pdf_response)

        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")

        return pdf_response

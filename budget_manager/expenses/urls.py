from django.urls import path
from expenses import views

app_name = "expenses"

urlpatterns = [
    path("expenses/", views.ExpenseListView.as_view(), name="expenses"),
    path("expenses/create/", views.ExpenseCreateView.as_view(), name="expense-create"),
    path(
        "expenses/<int:pk>/update/",
        views.ExpenseUpdateView.as_view(),
        name="expense-update",
    ),
    path("export-expenses-csv/", views.ExportExpensesCSVView.as_view(), name="export-expenses-csv"),
    path("export-expenses-pdf/", views.ExportExpensesPDFView.as_view(), name="export-expenses-pdf"),
]

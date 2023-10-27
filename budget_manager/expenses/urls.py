from django.urls import path
from expenses import views

app_name = "expenses"

urlpatterns = [
    path("expense/", views.ExpenseListView.as_view(), name="expenses"),
    path("expense/create/", views.ExpenseCreateView.as_view(), name="expense_create"),
    path("expense/update/<int:pk>", views.ExpenseUpdateView.as_view(), name="expense_update"),
]

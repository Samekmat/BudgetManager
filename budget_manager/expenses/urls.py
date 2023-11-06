from django.urls import path
from expenses import views

app_name = "expenses"

urlpatterns = [
    path("expenses/", views.ExpenseListView.as_view(), name="expenses"),
    path("expense/create/", views.ExpenseCreateView.as_view(), name="expense-create"),
    path("expense/<int:pk>/update/", views.ExpenseUpdateView.as_view(), name="expense-update"),
]

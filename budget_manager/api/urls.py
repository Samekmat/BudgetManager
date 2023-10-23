from api.views import ExpenseDeleteAPIView, IncomeDeleteAPIView
from django.urls import path

urlpatterns = [
    path("income/delete/<int:pk>/", IncomeDeleteAPIView.as_view(), name="api_income_delete"),
    path("expense/delete/<int:pk>/", ExpenseDeleteAPIView.as_view(), name="api_expense_delete"),
]

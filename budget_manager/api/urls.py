from django.urls import path
from api.views import IncomeDeleteAPIView, ExpenseDeleteAPIView


urlpatterns = [
    path('income/delete/<int:pk>/', IncomeDeleteAPIView.as_view(), name='api_income_delete'),
    path('expense/delete/<int:pk>/', ExpenseDeleteAPIView.as_view(), name='api_expense_delete'),

]

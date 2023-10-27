from api.views import CategoryDeleteAPIView, ExpenseDeleteAPIView, IncomeDeleteAPIView, TagDeleteAPIView
from django.urls import path

urlpatterns = [
    path("income/delete/<int:pk>/", IncomeDeleteAPIView.as_view(), name="api_income_delete"),
    path("expense/delete/<int:pk>/", ExpenseDeleteAPIView.as_view(), name="api_expense_delete"),
    path("category/delete/<int:pk>/", CategoryDeleteAPIView.as_view(), name="api_category_delete"),
    path("tag/delete/<int:pk>/", TagDeleteAPIView.as_view(), name="api_category_delete"),
]

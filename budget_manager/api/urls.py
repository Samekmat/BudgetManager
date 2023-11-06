from api.views import CategoryDeleteAPIView, ExpenseDeleteAPIView, IncomeDeleteAPIView, TagDeleteAPIView
from django.urls import path

urlpatterns = [
    path("income/<int:pk>/delete/", IncomeDeleteAPIView.as_view(), name="api-income-delete"),
    path("expense/<int:pk>/delete/", ExpenseDeleteAPIView.as_view(), name="api-expense-delete"),
    path("category/<int:pk>/delete/", CategoryDeleteAPIView.as_view(), name="api-category-delete"),
    path("tag/<int:pk>/delete/", TagDeleteAPIView.as_view(), name="api-tag-delete"),
]

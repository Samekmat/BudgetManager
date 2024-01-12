from api.views import (
    CategoryDeleteAPIView,
    ExpenseDeleteAPIView,
    IncomeDeleteAPIView,
    TagDeleteAPIView,
)
from django.urls import path

urlpatterns = [
    path(
        "incomes/<int:pk>/delete/",
        IncomeDeleteAPIView.as_view(),
        name="api-income-delete",
    ),
    path(
        "expenses/<int:pk>/delete/",
        ExpenseDeleteAPIView.as_view(),
        name="api-expense-delete",
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteAPIView.as_view(),
        name="api-category-delete",
    ),
    path("tags/<int:pk>/delete/", TagDeleteAPIView.as_view(), name="api-tag-delete"),
]

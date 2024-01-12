from django.urls import path
from incomes import views

app_name = "incomes"

urlpatterns = [
    path("incomes/", views.IncomeListView.as_view(), name="incomes"),
    path("incomes/create/", views.IncomeCreateView.as_view(), name="income-create"),
    path(
        "incomes/<int:pk>/update/",
        views.IncomeUpdateView.as_view(),
        name="income-update",
    ),
]

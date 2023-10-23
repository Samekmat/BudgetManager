from incomes import views
from django.urls import path

app_name = 'incomes'

urlpatterns = [
    path("income/", views.IncomeListView.as_view(), name="incomes"),
    path("income/create/", views.IncomeCreateView.as_view(), name="income_create"),
    path("income/update/<int:pk>", views.IncomeUpdateView.as_view(), name="income_update"),
]

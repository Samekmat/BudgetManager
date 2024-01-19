from budget_manager_app import views
from django.urls import path

app_name = "budgets"

urlpatterns = [
    path("budgets/", views.BudgetListView.as_view(), name="budgets"),
    path("budgets/create/", views.BudgetCreateView.as_view(), name="budget-create"),
    path(
        "budgets/<int:pk>/update/",
        views.BudgetUpdateView.as_view(),
        name="budget-update",
    ),
    path(
        "budgets/<int:pk>/delete/",
        views.BudgetDeleteView.as_view(),
        name="budget-delete",
    ),
    path(
        "budgets/<int:budget_id>/charts/",
        views.ChartView.as_view(),
        name="budget-chart",
    ),
    path(
        "budgets/<int:budget_id>/add-income-expense/",
        views.AddIncomeExpenseView.as_view(),
        name="add-income-expense",
    ),
    path("process-image/", views.ProcessImageView.as_view(), name="process_image"),
]

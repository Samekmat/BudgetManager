from django.urls import path

from budget_manager_app import views

app_name = "budgets"

urlpatterns = [
    path("budgets/", views.BudgetListView.as_view(), name="budgets"),
    path("budget/create/", views.BudgetCreateView.as_view(), name="budget-create"),
    path("budget/<int:pk>/update/", views.BudgetUpdateView.as_view(), name="budget-update"),
    path("budget/<int:pk>/delete/", views.BudgetDeleteView.as_view(), name="budget-delete"),
    path('budget/<int:budget_id>/charts/', views.ChartView.as_view(), name='budget-chart'),
    path('budget/<int:budget_id>/add-income-expense/', views.AddIncomeExpenseView.as_view(), name='add-income-expense'),
    ]

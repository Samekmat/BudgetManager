from django.urls import path

from budget_manager_app import views

app_name = "budgets"

urlpatterns = [
    path("goals/", views.SavingGoalListView.as_view(), name="goals"),
    path("goal/create/", views.SavingGoalCreateView.as_view(), name="goal-create"),
    path("goal/<int:pk>/update/", views.SavingGoalUpdateView.as_view(), name="goal-update"),
    path("goal/<int:pk>/detail/", views.SavingGoalDetailView.as_view(), name="goal-detail"),
    path("goal/<int:pk>/delete/", views.SavingGoalDeleteView.as_view(), name="goal-delete"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("budgets/", views.BudgetListView.as_view(), name="budgets"),
    path("budget/create/", views.BudgetCreateView.as_view(), name="budget-create"),
    path("budget/<int:pk>/update/", views.BudgetUpdateView.as_view(), name="budget-update"),
    path("budget/<int:pk>/delete/", views.BudgetDeleteView.as_view(), name="budget-delete"),
    path('budget/<int:budget_id>/charts/', views.ChartView.as_view(), name='budget-chart'),
    path('budget/<int:budget_id>/add-income-expense/', views.AddIncomeExpenseView.as_view(), name='add-income-expense'),
    ]

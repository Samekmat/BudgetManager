from django.urls import path

from saving_goals import views

app_name = "saving_goals"

urlpatterns = [
    path("goals/", views.SavingGoalListView.as_view(), name="goals"),
    path("goal/create/", views.SavingGoalCreateView.as_view(), name="goal-create"),
    path("goal/<int:pk>/update/", views.SavingGoalUpdateView.as_view(), name="goal-update"),
    path("goal/<int:pk>/detail/", views.SavingGoalDetailView.as_view(), name="goal-detail"),
    path("goal/<int:pk>/delete/", views.SavingGoalDeleteView.as_view(), name="goal-delete"),
    ]

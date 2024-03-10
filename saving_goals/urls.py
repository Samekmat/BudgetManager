from django.urls import path

from saving_goals import views

app_name = "saving_goals"

urlpatterns = [
    path("goals/", views.SavingGoalListView.as_view(), name="goals"),
    path("goals/create/", views.SavingGoalCreateView.as_view(), name="goal-create"),  # goal -> goals
    path(
        "goals/<int:pk>/update/",
        views.SavingGoalUpdateView.as_view(),
        name="goal-update",
    ),
    path(
        "goals/<int:pk>/detail/",
        views.SavingGoalDetailView.as_view(),
        name="goal-detail",
    ),
    path(
        "goals/<int:pk>/delete/",
        views.SavingGoalDeleteView.as_view(),
        name="goal-delete",
    ),
]

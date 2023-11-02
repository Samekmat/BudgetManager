"""URL configuration for budget_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from budget_manager_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("category/", views.CategoryListView.as_view(), name="categories"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category/update/<int:pk>", views.CategoryUpdateView.as_view(), name="category_update"),
    path("tag/", views.TagListView.as_view(), name="tags"),
    path("tag/create/", views.TagCreateView.as_view(), name="tag_create"),
    path("tag/update/<int:pk>", views.TagUpdateView.as_view(), name="tag_update"),
    path("goal/", views.SavingGoalListView.as_view(), name="goals"),
    path("goal/create/", views.SavingGoalCreateView.as_view(), name="goal_create"),
    path("goal/update/<int:pk>", views.SavingGoalUpdateView.as_view(), name="goal_update"),
    path("goal/delete/<int:pk>", views.SavingGoalDeleteView.as_view(), name="goal_delete"),
    path("dashboard/", views.DashboardListView.as_view(), name="dashboard"),
    # apps
    path("api/", include("api.urls")),
    path("users/", include("users.urls")),
    path("incomes/", include("incomes.urls")),
    path("expenses/", include("expenses.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path

from helper_models import views

app_name = "helper_models"

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path(
        "categories/<int:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tags/create/", views.TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", views.TagUpdateView.as_view(), name="tag-update"),
]

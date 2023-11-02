from django.urls import path
from helper_models import views

app_name = "helper_models"

urlpatterns = [
    path("category/", views.CategoryListView.as_view(), name="categories"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category/update/<int:pk>", views.CategoryUpdateView.as_view(), name="category_update"),
    path("tag/", views.TagListView.as_view(), name="tags"),
    path("tag/create/", views.TagCreateView.as_view(), name="tag_create"),
    path("tag/update/<int:pk>", views.TagUpdateView.as_view(), name="tag_update"),
]
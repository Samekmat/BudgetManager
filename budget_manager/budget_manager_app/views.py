from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from budget_manager_app.forms import CategoryForm, TagForm
from budget_manager_app.models import Category, Tag


def index(request):
    return render(request, "index.html")


class CategoryListView(ListView):
    model = Category
    template_name = "categories/categories.html"
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs["form"] = CategoryForm()
        return super().get_context_data(**kwargs)


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/categories.html"
    success_url = reverse_lazy("categories")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/edit_category.html"
    success_url = reverse_lazy("categories")

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.non_editable:
            messages.error(self.request, "Cannot edit a non-editable category.")
        return super().get(request, *args, **kwargs)


class TagListView(ListView):
    model = Tag
    template_name = "tags/tags.html"
    context_object_name = "tags"

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs["form"] = TagForm()
        return super().get_context_data(**kwargs)


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/tags.html"
    success_url = reverse_lazy("tags")

    def form_valid(self, form):
        messages.success(self.request, "Tag created successfully.")
        return super().form_valid(form)


class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/edit_tag.html"
    success_url = reverse_lazy("tags")

    def form_valid(self, form):
        messages.success(self.request, "Tag updated successfully.")
        return super().form_valid(form)

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from helper_models.forms import CategoryForm, TagForm
from helper_models.models import Category, Tag
from budget_manager_app.filters import CategoryFilter, TagFilter
from budget_manager_app.decorators import keep_parameters


@keep_parameters
class CategoryListView(ListView):
    model = Category
    template_name = "categories/categories.html"
    context_object_name = "categories"
    paginate_by = 5
    ordering = ['type']

    def get_queryset(self):
        category_filter = CategoryFilter(self.request.GET, queryset=super().get_queryset())
        return category_filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CategoryForm()
        context['filter'] = CategoryFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/categories.html"
    success_url = reverse_lazy("helper_models:categories")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/edit_category.html"
    success_url = reverse_lazy("helper_models:categories")

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.builtin:
            messages.error(self.request, "Cannot edit a non-editable category.")
            return HttpResponseRedirect(reverse("helper_models:categories"))  # Redirect to the category list page
        return super().post(request, *args, **kwargs)


@keep_parameters
class TagListView(ListView):
    model = Tag
    template_name = "tags/tags.html"
    context_object_name = "tags"
    paginate_by = 5
    ordering = ['name']

    def get_queryset(self):
        tag_filter = TagFilter(self.request.GET, queryset=super().get_queryset())
        return tag_filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TagForm()
        context['filter'] = TagFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/tags.html"
    success_url = reverse_lazy("helper_models:tags")

    def form_valid(self, form):
        messages.success(self.request, "Tag created successfully.")
        return super().form_valid(form)


class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/edit_tag.html"
    success_url = reverse_lazy("helper_models:tags")

    def form_valid(self, form):
        messages.success(self.request, "Tag updated successfully.")
        return super().form_valid(form)

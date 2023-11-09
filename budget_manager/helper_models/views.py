from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from helper_models.forms import CategoryForm, TagForm
from helper_models.models import Category, Tag
from budget_manager_app.filters import CategoryFilter, TagFilter
from budget_manager_app.decorators import keep_parameters


@keep_parameters
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "categories/categories.html"
    context_object_name = "categories"
    paginate_by = 5
    ordering = ['type']

    def get_queryset(self):
        user = self.request.user
        categories = Category.get_categories_for_user(user).order_by('type')
        return categories

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CategoryForm()

        # Apply the CategoryFilter on the filtered queryset
        filtered_queryset = CategoryFilter(self.request.GET, queryset=self.get_queryset()).qs

        # Paginate the filtered queryset
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)

        context['filter'] = CategoryFilter(self.request.GET, queryset=filtered_queryset)
        context['categories'] = categories
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/categories.html"
    success_url = reverse_lazy("helper_models:categories")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
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
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tags/tags.html"
    context_object_name = "tags"
    paginate_by = 5
    ordering = ['name']

    def get_queryset(self):
        user_tags = Tag.objects.filter(user=self.request.user).order_by('name')
        return user_tags

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TagForm()

        # Apply the TagFilter on the filtered queryset
        filtered_queryset = TagFilter(self.request.GET, queryset=self.get_queryset()).qs

        # Paginate the filtered queryset
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            tags = paginator.page(page)
        except PageNotAnInteger:
            tags = paginator.page(1)
        except EmptyPage:
            tags = paginator.page(paginator.num_pages)

        context['filter'] = TagFilter(self.request.GET, queryset=filtered_queryset)
        context['tags'] = tags

        return context


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/tags.html"
    success_url = reverse_lazy("helper_models:tags")

    def form_valid(self, form):
        messages.success(self.request, "Tag created successfully.")
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/edit_tag.html"
    success_url = reverse_lazy("helper_models:tags")

    def form_valid(self, form):
        messages.success(self.request, "Tag updated successfully.")
        return super().form_valid(form)
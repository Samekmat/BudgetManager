from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from budget_manager_app.forms import CategoryForm, TagForm, SavingGoalForm
from budget_manager_app.models import Category, Tag, SavingGoal


def index(request):
    return render(request, "index.html")


class CategoryListView(ListView):
    model = Category
    template_name = "categories/categories.html"
    context_object_name = "categories"
    paginate_by = 10
    ordering = ['type']

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
        obj = self.get_object()
        if obj.builtin:
            messages.error(self.request, "Cannot edit a non-editable category.")
        return super().get(request, *args, **kwargs)


class TagListView(ListView):
    model = Tag
    template_name = "tags/tags.html"
    context_object_name = "tags"
    paginate_by = 10
    ordering = ['name']

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


class SavingGoalListView(ListView):
    model = SavingGoal
    template_name = 'saving_goals/goals.html'
    context_object_name = 'goals'

    def post(self, request, *args, **kwargs):
        goal_id = request.POST.get('goal_id')
        goal = SavingGoal.objects.get(id=goal_id)

        if 'amount_to_add' in request.POST:
            amount_to_add = Decimal(request.POST.get('amount_to_add'))
            if amount_to_add > Decimal(0):
                goal.amount += amount_to_add
                messages.success(request, f"Added {amount_to_add} to the goal.")
            else:
                messages.error(request, "Invalid amount to add.")
        elif 'amount_to_subtract' in request.POST:
            amount_to_subtract = Decimal(request.POST.get('amount_to_subtract'))
            if goal.amount - amount_to_subtract >= Decimal(0):
                goal.amount -= amount_to_subtract
                messages.success(request, f"Subtracted {amount_to_subtract} from the goal.")
            else:
                messages.error(request, "Invalid amount to subtract")

        goal.save()
        return redirect('goals')


class SavingGoalCreateView(CreateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('goals')


class SavingGoalUpdateView(UpdateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = 'saving_goals/goal_form.html'
    success_url = reverse_lazy('goals')


class SavingGoalDeleteView(DeleteView):
    model = SavingGoal
    template_name = 'saving_goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goals')

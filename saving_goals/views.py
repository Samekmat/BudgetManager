from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from saving_goals.forms import SavingGoalForm
from saving_goals.models import SavingGoal


class SavingGoalListView(LoginRequiredMixin, ListView):
    model = SavingGoal
    template_name = "saving_goals/goals.html"
    context_object_name = "goals"

    def post(self, request, *args, **kwargs):
        goal_id = request.POST.get("goal_id")
        goal = SavingGoal.objects.get(id=goal_id)

        if "amount_to_add" in request.POST:
            amount_to_add = Decimal(request.POST.get("amount_to_add"))
            if amount_to_add > Decimal(0):
                goal.amount += amount_to_add
                messages.success(request, f"Added {amount_to_add}{goal.currency.symbol} to the goal.")
            else:
                messages.error(request, "Invalid amount to add.")
        elif "amount_to_subtract" in request.POST:
            amount_to_subtract = Decimal(request.POST.get("amount_to_subtract"))
            if amount_to_subtract > Decimal(0) and goal.amount - amount_to_subtract >= Decimal(0):
                goal.amount -= amount_to_subtract
                messages.success(
                    request,
                    f"Subtracted {amount_to_subtract}{goal.currency.symbol}  from the goal.",
                )
            else:
                messages.error(request, "Invalid amount to subtract.")

        goal.save()
        return redirect("saving_goals:goals")

    def get_queryset(self):
        user_goals = SavingGoal.objects.filter(user=self.request.user)
        return user_goals


class SavingGoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = "saving_goals/goal_form.html"
    success_url = reverse_lazy("saving_goals:goals")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Saving goal created successfully.")
        return super().form_valid(form)


class SavingGoalUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = "saving_goals/goal_form.html"
    success_url = reverse_lazy("saving_goals:goals")

    def form_valid(self, form):
        messages.success(self.request, "Saving goal updated successfully.")
        return super().form_valid(form)

    def get_queryset(self):
        user_goals = SavingGoal.objects.filter(user=self.request.user)
        return user_goals


class SavingGoalDetailView(LoginRequiredMixin, DetailView):
    model = SavingGoal
    template_name = "saving_goals/goal_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to access this goal.")
        return obj


class SavingGoalDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingGoal
    template_name = "saving_goals/goal_confirm_delete.html"
    success_url = reverse_lazy("saving_goals:goals")

    def delete(self, request, *args, **kwargs):
        goal = self.get_object()
        if goal.user == self.request.user:
            messages.success(self.request, "Saving goal deleted successfully.")
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to delete this goal.")

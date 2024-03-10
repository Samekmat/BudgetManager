from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response

from api.serializers import (
    CategorySerializer,
    ExpenseSerializer,
    IncomeSerializer,
    TagSerializer,
)
from expenses.models import Expense
from helper_models.models import Category, Tag
from incomes.models import Income


class IncomeDeleteAPIView(generics.DestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            idx = instance.id
            self.perform_destroy(instance)
            messages.success(request, f"Income with ID {idx} has been deleted.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "You do not have permission to delete this income."},
                status=status.HTTP_403_FORBIDDEN,
            )


class ExpenseDeleteAPIView(generics.DestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        idx = instance.id
        self.perform_destroy(instance)
        messages.success(request, f"Expense with ID {idx} has been deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        idx = instance.id

        if instance.builtin:
            msg = f"Cannot delete a non-editable category with ID {idx}."
            messages.error(request, msg)
            return Response(data={"message": msg}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        messages.success(request, f"Category with ID {idx} has been deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagDeleteAPIView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        idx = instance.id
        self.perform_destroy(instance)
        messages.success(request, f"Tag with ID {idx} has been deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)

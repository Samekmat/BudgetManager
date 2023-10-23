from api.serializers import ExpenseSerializer, IncomeSerializer
from expenses.models import Expense
from incomes.models import Income
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response


class IncomeDeleteAPIView(generics.DestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        idx = instance.id
        self.perform_destroy(instance)
        messages.success(request, f"Income with ID {idx} has been deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseDeleteAPIView(generics.DestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        idx = instance.id
        self.perform_destroy(instance)
        messages.success(request, f"Expense with ID {idx} has been deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)

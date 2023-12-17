from expenses.models import Expense
from helper_models.models import Category
from incomes.models import Income
from rest_framework import serializers


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description", "is_income")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)

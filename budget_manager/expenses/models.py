from budget_manager_app.consts import PAYMENT_METHOD_CHOICES
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from helper_models.models import Category, Currency, Tag


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "expense"},
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default="cash")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="expense_images/", blank=True, null=True)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return f"Expense-{self.pk}({self.user.username}) - {self.amount}{self.currency.symbol}"

    @staticmethod
    def compare_expenses(request):
        user = request.user

        today = timezone.now()
        first_day_previous_month = timezone.datetime(today.year, today.month, 1) - timezone.timedelta(days=1)

        results = {}

        distinct_currencies = Currency.objects.filter(expense__user=user).distinct()

        for category in Category.objects.filter(type="expense"):
            category_results = {}

            for currency in distinct_currencies:
                total_expenses = (
                    Expense.objects.filter(
                        user=user,
                        category=category,
                        currency=currency,
                        date__range=(first_day_previous_month, today),
                    ).aggregate(Sum("amount"))["amount__sum"]
                    or 0
                )

                total_entire_period = (
                    Expense.objects.filter(
                        user=user,
                        category=category,
                        currency=currency,
                        date__lte=today,
                    ).aggregate(
                        Sum("amount")
                    )["amount__sum"]
                    or 0
                )

                if total_expenses > total_entire_period:
                    result = "increased"
                elif total_expenses < total_entire_period:
                    result = "decreased"
                else:
                    result = "unchanged"

                percentage_change = 0
                if total_entire_period != 0:
                    percentage_change = ((total_expenses - total_entire_period) / total_entire_period) * 100

                category_results[currency.symbol] = {"result": result, "percentage_change": percentage_change}

            results[category.name] = category_results

        return results

    @staticmethod
    def forecast_expenses(request):
        user = request.user

        today = timezone.now()

        results = {}

        distinct_currencies = Currency.objects.filter(expense__user=user).distinct()

        for category in Category.objects.filter(type="expense"):
            category_results = {}

            for currency in distinct_currencies:
                expenses = Expense.objects.filter(user=user, category=category, currency=currency, date__lte=today)

                monthly_totals = (
                    expenses.annotate(year_month=TruncMonth("date")).values("year_month").annotate(total=Sum("amount"))
                )

                total_months = len(monthly_totals)
                total_amount = sum(item["total"] for item in monthly_totals)

                average_amount_per_month = 0
                if total_months != 0:
                    average_amount_per_month = total_amount / total_months

                category_results[currency.symbol] = {"average_amount_per_month": average_amount_per_month}

            results[category.name] = category_results

        return results

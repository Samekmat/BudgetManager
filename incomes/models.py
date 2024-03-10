from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from budget_manager_app.consts import PAYMENT_METHOD_CHOICES
from helper_models.models import Category, Currency, Tag


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "income"},
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default="cash")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="income_images/", blank=True, null=True)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return f"Income-{self.pk}({self.user.username}) - {self.amount}{self.currency.symbol}"

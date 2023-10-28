from budget_manager_app.models import PAYMENT_METHOD_CHOICES, Category, Currency, Tag
from django.db import models
from users.models import User


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, limit_choices_to={"type": "Income"}, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default="cash")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="income_images/", blank=True, null=True)

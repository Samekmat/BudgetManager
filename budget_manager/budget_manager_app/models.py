from django.db import models

from helper_models.models import Currency


class SavingGoal(models.Model):
    name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

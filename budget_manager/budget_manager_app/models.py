from django.db import models
from django.contrib.auth.models import User


PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    category = models.ForeignKey('CategoryIncome', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cash')
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField('Tag', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='income_images/', blank=True, null=True)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    category = models.ForeignKey('CategoryExpense', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cash')
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField('Tag', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='expense_images/', blank=True, null=True)


class CategoryExpense(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.name


class CategoryIncome(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

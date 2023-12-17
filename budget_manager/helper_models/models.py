from budget_manager_app.choices import CATEGORY_TYPES
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=60, choices=CATEGORY_TYPES)
    builtin = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def delete(self, *args, **kwargs):
        if not self.builtin:
            super(Category, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.builtin:
            super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @staticmethod
    def get_categories_for_user(user):
        if user.is_authenticated:
            return Category.objects.filter(Q(user=user) | Q(builtin=True))
        else:
            return Category.objects.filter(builtin=True)


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

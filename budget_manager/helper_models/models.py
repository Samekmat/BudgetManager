from django.db import models

from budget_manager_app.choices import CATEGORY_TYPES


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=60, choices=CATEGORY_TYPES)
    builtin = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if not self.builtin:
            super(Category, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.builtin:
            super(Category, self).save(*args, **kwargs)

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

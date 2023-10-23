from django.contrib import admin
from budget_manager_app.models import Income, CategoryIncome, CategoryExpense
# Register your models here.
admin.site.register(Income)
admin.site.register(CategoryIncome)
admin.site.register(CategoryExpense)
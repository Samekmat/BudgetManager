# Generated by Django 4.2.3 on 2023-10-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "budget_manager_app",
            "0011_savinggoal_remove_category_is_income_category_type",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="type",
            field=models.CharField(
                choices=[("income", "Income"), ("expense", "Expense")], max_length=60
            ),
        ),
    ]
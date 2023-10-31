# Generated by Django 4.2.3 on 2023-10-30 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "budget_manager_app",
            "0011_savinggoal_remove_category_is_income_category_type",
        ),
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"type": "Expense"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="budget_manager_app.category",
            ),
        ),
    ]
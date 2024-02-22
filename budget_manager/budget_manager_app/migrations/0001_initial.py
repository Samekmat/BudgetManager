# Generated by Django 5.0 on 2024-02-02 18:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("expenses", "0001_initial"),
        ("helper_models", "0001_initial"),
        ("incomes", "__first__"),
        ("saving_goals", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                (
                    "currency",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helper_models.currency",
                    ),
                ),
                ("expenses", models.ManyToManyField(to="expenses.expense")),
                (
                    "goals",
                    models.ManyToManyField(blank=True, to="saving_goals.savinggoal"),
                ),
                ("incomes", models.ManyToManyField(to="incomes.income")),
                (
                    "shared_with",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Users with whom the budget is shared",
                        related_name="shared_budgets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User who owns the budget",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="budgets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]

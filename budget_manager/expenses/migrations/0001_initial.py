# Generated by Django 4.2.3 on 2023-10-23 17:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("budget_manager_app", "0008_category_remove_expense_category_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("credit_card", "Credit Card"),
                            ("bank_transfer", "Bank Transfer"),
                            ("paypal", "PayPal"),
                        ],
                        default="cash",
                        max_length=30,
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="expense_images/"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"is_income": False},
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="budget_manager_app.category",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="budget_manager_app.currency",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(blank=True, null=True, to="budget_manager_app.tag"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
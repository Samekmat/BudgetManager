# Generated by Django 5.0 on 2024-02-05 17:17

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("helper_models", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Income",
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
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("date", models.DateField()),
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
                    models.ImageField(blank=True, null=True, upload_to="income_images/"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        limit_choices_to={"type": "income"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helper_models.category",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helper_models.currency",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="helper_models.tag")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("date",),
            },
        ),
    ]

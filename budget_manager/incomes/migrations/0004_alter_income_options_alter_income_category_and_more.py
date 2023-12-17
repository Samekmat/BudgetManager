# Generated by Django 4.2.6 on 2023-11-02 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("helper_models", "0001_initial"),
        ("incomes", "0003_alter_income_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="income",
            options={"ordering": ("date",)},
        ),
        migrations.AlterField(
            model_name="income",
            name="category",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"type": "income"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="helper_models.category",
            ),
        ),
        migrations.AlterField(
            model_name="income",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="helper_models.currency",
            ),
        ),
        migrations.AlterField(
            model_name="income",
            name="tags",
            field=models.ManyToManyField(blank=True, null=True, to="helper_models.tag"),
        ),
    ]

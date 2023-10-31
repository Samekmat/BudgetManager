# Generated by Django 4.2.3 on 2023-08-21 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "budget_manager_app",
            "0002_categoryexpense_categoryincome_currency_tag_income_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="budget_manager_app.categoryexpense",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="budget_manager_app.currency",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="expense",
            name="description",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="expense",
            name="tags",
            field=models.ManyToManyField(blank=True, null=True, to="budget_manager_app.tag"),
        ),
        migrations.AlterField(
            model_name="income",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="budget_manager_app.categoryincome",
            ),
        ),
        migrations.AlterField(
            model_name="income",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="budget_manager_app.currency",
            ),
        ),
        migrations.AlterField(
            model_name="income",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="income",
            name="tags",
            field=models.ManyToManyField(blank=True, null=True, to="budget_manager_app.tag"),
        ),
    ]
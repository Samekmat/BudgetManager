# Generated by Django 4.2.3 on 2023-10-30 21:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget_manager_app", "0013_savinggoal_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="savinggoal",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="savinggoal",
            name="goal",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-28 16:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("budget_manager_app", "0019_savinggoal_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="savinggoal",
            name="currency",
        ),
        migrations.RemoveField(
            model_name="savinggoal",
            name="user",
        ),
    ]

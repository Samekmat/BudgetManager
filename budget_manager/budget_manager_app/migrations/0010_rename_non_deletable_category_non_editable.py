# Generated by Django 4.2.3 on 2023-10-27 06:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("budget_manager_app", "0009_category_non_deletable"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="non_deletable",
            new_name="builtin",
        ),
    ]
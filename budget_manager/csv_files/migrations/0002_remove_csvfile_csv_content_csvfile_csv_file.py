# Generated by Django 5.0 on 2024-01-25 19:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("csv_files", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="csvfile",
            name="csv_content",
        ),
        migrations.AddField(
            model_name="csvfile",
            name="csv_file",
            field=models.FileField(default=django.utils.timezone.now, upload_to="csv_files/"),
            preserve_default=False,
        ),
    ]
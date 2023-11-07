# Generated by Django 4.2.6 on 2023-11-07 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helper_models', '0002_category_user_tag_user'),
        ('budget_manager_app', '0017_budget_goals'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='helper_models.currency'),
        ),
        migrations.AlterField(
            model_name='budget',
            name='goals',
            field=models.ManyToManyField(blank=True, to='budget_manager_app.savinggoal'),
        ),
    ]

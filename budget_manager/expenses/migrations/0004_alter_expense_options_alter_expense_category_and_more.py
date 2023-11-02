# Generated by Django 4.2.6 on 2023-11-02 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helper_models', '0001_initial'),
        ('expenses', '0003_alter_expense_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ('date',)},
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'expense'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='helper_models.category'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helper_models.currency'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='helper_models.tag'),
        ),
    ]

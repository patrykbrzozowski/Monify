# Generated by Django 4.0.5 on 2022-10-14 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0011_income_income_value_non_negative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='balance',
            field=models.ForeignKey(limit_choices_to={'type': 1}, on_delete=django.db.models.deletion.CASCADE, to='finances.balance'),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='balance',
            field=models.ForeignKey(limit_choices_to={'type': 1}, on_delete=django.db.models.deletion.CASCADE, to='finances.balance'),
        ),
    ]

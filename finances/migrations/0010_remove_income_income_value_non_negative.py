# Generated by Django 4.0.5 on 2022-09-10 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0009_alter_income_value_income_income_value_non_negative'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='income',
            name='income_value_non_negative',
        ),
    ]

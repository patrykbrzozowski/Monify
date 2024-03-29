# Generated by Django 4.0.5 on 2022-09-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0008_remove_income_income_value_non_negative_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AddConstraint(
            model_name='income',
            constraint=models.CheckConstraint(check=models.Q(('value__gte', '0')), name='income_value_non_negative'),
        ),
    ]

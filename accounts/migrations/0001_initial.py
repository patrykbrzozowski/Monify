# Generated by Django 4.0.5 on 2022-09-01 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('PLN', 'zł'), ('EUR', '€'), ('USD', '$'), ('NOK', 'Kr'), ('CHF', 'Fr'), ('GBP', '£'), ('JPY', '¥'), ('GBP', '£'), ('HRK', 'KN'), ('HUF', 'Ft'), ('CZK', 'Kč')], default='PLN', max_length=6, null=True)),
                ('saving_method', models.CharField(choices=[('METODA 6 SŁOIKÓW', 'METODA 6 SŁOIKÓW'), ('METODA 50/30/20', 'METODA 50/30/20')], default='METODA 6 SŁOIKÓW', max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

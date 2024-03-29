# Generated by Django 4.0.5 on 2022-07-10 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finances', '0002_alter_balance_options_alter_balance_type_outcome'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Prezent'), (2, 'Pensja'), (3, 'Bonus'), (4, 'Nagroda'), (5, 'Zwrot'), (6, 'Oszczędności'), (7, 'Inne')])),
                ('date', models.DateField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.balance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'incomes',
                'ordering': ['-date'],
            },
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-28 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balance',
            options={'ordering': ['-date'], 'verbose_name_plural': 'balances'},
        ),
        migrations.AlterField(
            model_name='balance',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Standardowe'), (2, 'Oszczędnościowe')]),
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Opłata za mieszkanie'), (2, 'Spłata kredytów'), (3, 'Rachunki'), (4, 'Higiena'), (5, 'Koszty leczenia i leki'), (6, 'Kosmetyki'), (7, 'Wydatki na szkołe i przedszkole'), (8, 'Jedzenie i picie'), (9, 'Transport'), (10, 'Ubezpieczenie'), (11, 'Samochód'), (12, 'Parking i opłaty'), (13, 'Karma dla zwierząt'), (14, 'Duże zakupy'), (15, 'Remont'), (16, 'Wymiana sprzętów domowych'), (17, 'Wakacje'), (18, 'Niespodziewane wydatki(np. naprawa samochodu)'), (19, 'Mandat'), (20, 'Kary'), (21, 'Restauracje'), (22, 'Puby i bary'), (23, 'Kluby'), (24, 'Filmy'), (25, 'Gry'), (26, 'Muzyka'), (27, 'Subskrypcje'), (28, 'Elektronika'), (29, 'Kino i teatr'), (30, 'Wyjście ze znajomymi'), (31, 'Zabawa'), (32, 'Koncert'), (33, 'Rozrywka'), (34, 'Dekoracje'), (35, 'Meble'), (36, 'Atrakcje/wypoczynek'), (37, 'Zakupy'), (38, 'Książki'), (39, 'Kursy'), (40, 'Szkolenia'), (41, 'Mentoring'), (42, 'Akcje'), (43, 'Kryptowaluty'), (44, 'Nieruchomości'), (45, 'Dochód pasywny'), (46, 'Fundusze'), (47, 'Oszczędności'), (48, 'Wpłata na lokate'), (49, 'Surowce'), (50, 'Obligacje'), (51, 'Datki na fundacje'), (52, 'Pomoc potrzebującym'), (53, 'Prezenty')])),
                ('date', models.DateField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.balance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outcomes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'outcomes',
                'ordering': ['-date'],
            },
        ),
    ]

# Generated by Django 4.0.5 on 2022-09-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_alter_balance_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Opłata za mieszkanie'), (2, 'Spłata kredytów'), (3, 'Rachunki'), (4, 'Higiena'), (5, 'Koszty leczenia i leki'), (6, 'Kosmetyki'), (7, 'Wydatki na szkołe i przedszkole'), (8, 'Jedzenie i picie'), (9, 'Transport'), (10, 'Ubezpieczenie'), (11, 'Samochód'), (12, 'Parking i opłaty'), (13, 'Karma dla zwierząt'), (14, 'Duże zakupy'), (15, 'Remont'), (16, 'Wymiana sprzętów domowych'), (17, 'Wakacje'), (18, 'Niespodziewane wydatki(np. naprawa samochodu)'), (19, 'Mandat'), (20, 'Kary'), (21, 'Restauracje'), (22, 'Puby i bary'), (23, 'Kluby'), (24, 'Filmy'), (25, 'Gry'), (26, 'Muzyka'), (27, 'Subskrypcje'), (28, 'Elektronika'), (29, 'Kino i teatr'), (30, 'Wyjście ze znajomymi'), (31, 'Zabawa'), (32, 'Koncert'), (33, 'Rozrywka'), (34, 'Dekoracje'), (35, 'Meble'), (36, 'Atrakcje/wypoczynek'), (37, 'Zakupy'), (38, 'Książki'), (39, 'Kursy'), (40, 'Szkolenia'), (41, 'Mentoring'), (42, 'Akcje'), (43, 'Kryptowaluty'), (44, 'Nieruchomości'), (45, 'Dochód pasywny'), (46, 'Fundusze'), (47, 'Oszczędności'), (48, 'Wpłata na lokate'), (49, 'Surowce'), (50, 'Waluty'), (51, 'Obligacje'), (52, 'Datki na fundacje'), (53, 'Pomoc potrzebującym'), (54, 'Prezenty')]),
        ),
    ]

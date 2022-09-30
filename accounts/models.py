from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    CURRENCIES = [
        ('PLN', 'zł'),
        ('EUR', '€'),
        ('USD', '$'),
        ('NOK', 'Kr'),
        ('CHF', 'Fr'),
        ('GBP', '£'),
        ('JPY', '¥'),
        ('GBP', '£'),
        ('HRK', 'KN'),
        ('HUF', 'Ft'),
        ('CZK', 'Kč')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=6, null=True, choices=CURRENCIES, default=CURRENCIES[0][0])
    saving_method = models.CharField(max_length=30, null=True, choices=[('METODA 6 SŁOIKÓW', 'METODA 6 SŁOIKÓW'), ('METODA 50/30/20', 'METODA 50/30/20')], default='METODA 6 SŁOIKÓW')

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User


# Balance model
class Balance(models.Model):
    
    class BTypes(models.IntegerChoices):
        STA = 1, "Standardowe"
        OSZ = 2, "Oszczędnościowe"
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances')
    name = models.CharField(max_length=60)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=BTypes.choices)
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.value}"

    class Meta:
        verbose_name_plural = 'balances'
        ordering = ['-date']
        

# Outcome model
class Outcome(models.Model):
    class OTypes(models.IntegerChoices):
        OPM = 1, "Opłata za mieszkanie"
        SPK = 2, "Spłata kredytów"
        RAC = 3, "Rachunki"
        HIG = 4, "Higiena"
        LEK = 5, "Koszty leczenia i leki"
        KOS = 6, "Kosmetyki"
        SZP = 7, "Wydatki na szkołe i przedszkole"
        JED = 8, "Jedzenie i picie"
        TRA = 9, "Transport"
        UBE = 10, "Ubezpieczenie"
        SAM = 11, "Samochód"
        PAR = 12, "Parking i opłaty"
        ZWI = 13, "Karma dla zwierząt"
        DUZ = 14, "Duże zakupy"
        REM = 15, "Remont"
        SPR = 16, "Wymiana sprzętów domowych"
        WAK = 17, "Wakacje"
        NIW = 18, "Niespodziewane wydatki(np. naprawa samochodu)"
        MAN = 19, "Mandat"
        KAR = 20, "Kary"
        RES = 21, "Restauracje"
        PUB = 22, "Puby i bary"
        KLU = 23, "Kluby"
        FIL = 24, "Filmy"
        GRY = 25, "Gry"
        MUZ = 26, "Muzyka"
        SUB = 27, "Subskrypcje"
        ELE = 28, "Elektronika"
        KIN = 29, "Kino i teatr"
        WYJ = 30, "Wyjście ze znajomymi"
        ZAB = 31, "Zabawa"
        KON = 32, "Koncert"
        ROZ = 33, "Rozrywka"
        DEK = 34, "Dekoracje"
        MEB = 35, "Meble"
        ATR = 36, "Atrakcje/wypoczynek"
        ZAK = 37, "Zakupy"
        KSI = 38, "Książki"
        KUR = 39, "Kursy"
        SZK = 40, "Szkolenia"
        MEN = 41, "Mentoring"
        AKC = 42, "Akcje"
        KRY = 43, "Kryptowaluty"
        NIE = 44, "Nieruchomości"
        DOP = 45, "Dochód pasywny"
        FUN = 46, "Fundusze"
        OSZ = 47, "Oszczędności"
        WPL = 48, "Wpłata na lokate"
        SUR = 49, "Surowce"
        WAL = 50, "Waluty"
        OBL = 51, "Obligacje"
        DAT = 52, "Datki na fundacje"
        POM = 53, "Pomoc potrzebującym"
        PRE = 54, "Prezenty"
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outcomes')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=OTypes.choices)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.value}"

    class Meta:
        verbose_name_plural = 'outcomes'
        ordering = ['-date', '-created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(value__gte='0'), name='outcome_value_non_negative'),
        ]


# Income model
class Income(models.Model):
    class ITypes(models.IntegerChoices):
        PRE = 1, "Prezent"
        PEN = 2, "Pensja"
        BON = 3, "Bonus"
        NAG = 4, "Nagroda"
        ZWR = 5, "Zwrot"
        OSZ = 6, "Oszczędności"
        INN = 7, "Inne"
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=ITypes.choices)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.value}"

    class Meta:
        verbose_name_plural = 'incomes'
        ordering = ['-date', '-created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(value__gte='0'), name='income_value_non_negative'),
        ]

from django.contrib import admin
from finances.models import Balance, Outcome, Income


admin.site.register(Balance)
admin.site.register(Outcome)
admin.site.register(Income)

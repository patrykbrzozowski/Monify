from django import forms
from datetime import date

from .models import Balance, Outcome, Income

class DateInput(forms.DateInput):
    input_type = 'date'

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['name', 'value', 'date', 'type', 'comment']
        
    date = forms.DateField(widget=DateInput, initial=date.today())

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['value', 'date', 'type', 'balance', 'comment']

    def is_valid(self):
        is_valid = super().is_valid()
        value = self.cleaned_data.get('value')

        if value <= 0:
            self.add_error('value', 'Wartość nie może być mniejsza niż 0.')
            is_valid = False
        
        return is_valid
        
    date = forms.DateField(widget=DateInput, initial=date.today())

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['value', 'date', 'type', 'balance', 'comment']

    def is_valid(self):
        is_valid = super().is_valid()
        value = self.cleaned_data.get('value')

        if value <= 0:
            self.add_error('value', 'Wartość nie może być mniejsza niż 0.')
            is_valid = False
        
        return is_valid

    date = forms.DateField(widget=DateInput, initial=date.today())

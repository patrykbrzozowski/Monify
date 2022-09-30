from django import forms
from datetime import date

from .models import Balance, Outcome, Income

class DateInput(forms.DateInput):
    input_type = 'date'


# class IncomeOutcomeForm(forms.ModelForm):
#     def is_valid(self):
#         is_valid = super().is_valid()

#         value = self.cleaned_data.get('value')
#         form_date = self.cleaned_data.get('date')
#         repetitive = self.cleaned_data.get('repetitive')
#         repetition_interval = self.cleaned_data.get('repetition_interval')
#         repetition_time = self.cleaned_data.get('repetition_time')
#         repetition_end = self.cleaned_data.get('repetition_end')

#         if value <= 0:
#             self.add_error('value', 'Value must be a positive number')
#             is_valid = False
        
#         if repetition_interval == 4 and form_date.day > 28:     # if it's MONTHS and date is set for over 28th
#             self.add_error('date', 'When repetiotion interval is set to MONTHS, date can not exceed 28.')
#             is_valid = False

#         if repetitive:
#             if repetition_interval == 1:     # if it's N/A
#                 self.add_error('repetition_interval', 'Repetition interval can not be N/A when Repetition is selected')
#                 is_valid = False
#             if repetition_time == 0:
#                 self.add_error('repetition_time', 'Repetition time can not be 0 when Repetition is selected')
#                 is_valid = False
#             if form_date and repetition_end:
#                 if repetition_end <= form_date:
#                     self.add_error('repetition_end', 'Repetition end date cant be before or on the Date')
#                     is_valid = False
#         else:   # if Repetition is False
#             if repetition_interval != 1:
#                 self.add_error('repetitive', 'Repetitive needs to be selected when Repetition interval is not N/A')
#                 is_valid = False
#             if repetition_time != 0:
#                 self.add_error('repetition_time', 'Repetitions need to be selected when Repetition time is no 0')
#                 is_valid = False
#             if repetition_end:
#                 self.add_error('repetition_end', 'Repetitive needs to be selected when repetition end is not empty')
#                 is_valid = False
        
#         return is_valid



class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['name', 'value', 'date', 'type', 'comment']
        
    date = forms.DateField(widget=DateInput, initial=date.today())

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['value', 'date', 'type', 'balance', 'comment']
        
    date = forms.DateField(widget=DateInput, initial=date.today())

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['value', 'date', 'type', 'balance', 'comment']

    # def is_valid(self):
    #     is_valid = super().is_valid()

    #     value = self.cleaned_data.get('value')

    #     if value <= 0:
    #         self.add_error('value', 'Value must be a positive number')
    #         is_valid = False
        
        
    #     return is_valid

    def clean_value(self, *args, **kwargs):
        value = self.cleaned_data.get('value')

        if value <= 0:
            raise forms.ValidationError('This is not valid value')
            
        return value

        
    date = forms.DateField(widget=DateInput, initial=date.today())

# class ChoseYearForm(forms.Form):

#     dates = Income.objects.filter(user__id=2)\
#                        .annotate(year=ExtractYear('date'))\
#                        .values('year').order_by('-year')

#     for year in dates:
#         print(year)

#     YEAR_CHOICES = [
#         (year['year'], year['year']) for year in dates
#     ]

#     year = forms.ModelMultipleChoiceField(queryset=Income.objects.filter(user__id=1)\
#                        .annotate(year=ExtractYear('date'))\
#                        .values('year').order_by('-year'))

#     def __init__(self, user, *args, **kwargs):
#         super(ChoseYearForm, self).__init__(*args, **kwargs)
#         self.fields['year'].queryset = User.objects.filter(pk = user.id)


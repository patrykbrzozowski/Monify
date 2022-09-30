from base64 import encode
import calendar
from decimal import Decimal
# from distutils.log import Log
# from dateutil import rrule
from dateutil import relativedelta
from datetime import date, timedelta, datetime
from django.utils.formats import date_format
from django.utils import translation
import json
import io
import csv
import locale
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont   
import time
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q, Count
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
# from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import BalanceForm, OutcomeForm, IncomeForm
from .models import Balance, Outcome, Income
from accounts.models import Account

# Balance Views
class BalanceListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Balance
    paginate_by = 10
    template_name = 'finances/balance_list.html'

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)

    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super(BalanceListView,self).get_context_data(**kwargs)
        if Balance.objects.filter(user=user).exists():
            context['data_exist'] = True
        context['list_what'] = 'Balance'
        return context

    # def get(self, request):
    #     user = request.user
    #     balances = Balance.objects.filter()
    #     data = []
    #     for balance in balances:
    #         data.append({
    #             'id': balance.id,
    #             'name': balance.name,
    #             'value': balance.value,
    #             'created_at': balance.created_at.date().strftime("%d/%m/%y"),
    #             'type': balance.type
    #         })
    #     return JsonResponse(data, safe=False)

# def balance_list_get(request):
#     return render(request, 'finances/balance_list.html', {'balances': Balance.objects.all(),})

class BalanceDetailView(DetailView):
    model = Balance
    template_name = 'finances/balance_income_outcome_detail.html'
    extra_context = {'detail_what': 'Balance'}

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)

class BalanceCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    model = Balance
    form_class = BalanceForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Dodaj konto'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{self.object.name} added."
                    })
                })


class BalanceUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Balance
    form_class = BalanceForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Edytuj konto'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{self.object.name} added."
                    })
                })


@login_required(login_url='accounts:login')
def balance_list(request):
    return render(request, 'finances/balance_income_outcome_list.html')

@login_required(login_url='accounts:login')
def delete_balance(request, part_id=None):
    balance = Balance.objects.filter(id=part_id)
    if request.method == "POST":
        balance.delete()
        return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "movieListChanged": None,
                        })
                    })
    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model':'konto', 'model_name':balance[0].name})


# def balances_list(request):
#     balances = [{
#         'id': balance.id,
#         'name': balance.name,
#         'created_at': balance.created_at,
#         'value': balance.value
#     } for balance in Balance.objects.filter(user=request.user)]

#     return JsonResponse(status=200, data=balances, safe=False)

# def create_balance(request):
#     user = request.user
#     name = request.POST.get('user')
#     value = request.POST.get('value')
#     type = request.POST.get('type')
#     date = request.POST.get('date')
#     comment = request.POST.get('comment')
#     print(name)
#     if not name:
#         return JsonResponse(status=400, data={'error': 'title is required'})
#     task = Balance.objects.create(name=name, user=user, value=value, type=type, date=date, comment=comment)
#     return JsonResponse(status=201, data={'name': task.name,
#                                           'id': task.id}, safe=False)


# Outcome Views

class OutcomeListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Outcome
    paginate_by = 15
    template_name = 'finances/balance_list.html'

    def get_queryset(self):
        user = self.request.user
        return Outcome.objects.filter(user=user)

    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super(OutcomeListView,self).get_context_data(**kwargs)
        if Outcome.objects.filter(user=user).exists():
            context['data_exist'] = True
        context['list_what'] = 'Outcome'
        return context

class OutcomeCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    model = Outcome
    form_class = OutcomeForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Dodaj wydatek'}

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['balance'].limit_choices_to = {'user': self.request.user}
        return modelform


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        balance = Balance.objects.filter(id=self.object.balance.id)
        balance_value = balance.aggregate(total=Sum('value'))['total']
        balance_value -= self.object.value
        balance.update(value = balance_value)
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{self.object.comment} added."
                    })
                })



class OutcomeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Outcome
    form_class = OutcomeForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Edytuj wydatek'}

    # def clean_value(self):
    #     data = Outcome.objects.filter(id=self.id)
    #     print(data)
    #     return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        old_outcome_value = Outcome.objects.filter(id=self.object.id).aggregate(total=Sum('value'))['total']
        old_outcome_balance = Outcome.objects.filter(id=self.object.id).values('balance_id')[0]['balance_id']
        print(old_outcome_balance)
        # print(old_outcome_value)
        self.object.save()
        # print(self.object.value)
        # print(self.object.balance.id)
        balance = Balance.objects.filter(id=self.object.balance.id)
        balance_value = balance.aggregate(total=Sum('value'))['total']
        value_to_substract = self.object.value - old_outcome_value
        print(value_to_substract)

        if old_outcome_balance != self.object.balance.id:
            old_balance = Balance.objects.filter(id = old_outcome_balance)
            old_balance_value = old_balance.aggregate(total=Sum('value'))['total']
            old_balance_value += old_outcome_value
            old_balance.update(value = old_balance_value)
            value_to_substract = self.object.value

        print(value_to_substract)
        balance_value -= value_to_substract
        # print(value_to_substract)
        balance.update(value = balance_value)
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{self.object.comment} added."
                    })
                })

def delete_outcome(request, part_id=None):
    outcome = Outcome.objects.filter(id=part_id)
    outcome1 = outcome.get()
    outcome_value = outcome.aggregate(total=Sum('value'))['total']
    balance = Balance.objects.filter(id=outcome1.balance.id)
    balance_value = balance.aggregate(total=Sum('value'))['total']

    if request.method == "POST":
        outcome.delete()
        balance_value += outcome_value
        balance.update(value = balance_value)
        return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "movieListChanged": None,
                        })
                    })
    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model': 'wydatek','model_name':outcome[0].get_type_display, 'model_value':outcome[0].value, 'model_date': outcome[0].date})

def outcome_list(request):
    return render(request, 'finances/outcome_list.html', context={'list_what': 'Wydatki'})


# Income Views

class IncomeListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Income
    paginate_by = 15
    template_name = 'finances/balance_list.html'

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)

    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super(IncomeListView,self).get_context_data(**kwargs)
        if Income.objects.filter(user=user).exists():
            context['data_exist'] = True
        context['list_what'] = 'Income'
        return context

class IncomeCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    model = Income
    form_class = IncomeForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Dodaj przychód'}

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['balance'].limit_choices_to = {'user': self.request.user}
        return modelform


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        balance = Balance.objects.filter(id=self.object.balance.id)
        balance_value = balance.aggregate(total=Sum('value'))['total']
        balance_value += self.object.value
        balance.update(value = balance_value)
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{self.object.comment} added."
                    })
                })

    # def create_valid_form(request):
    #     value = request.POST.get('value')
    #     if value < 0:
    #         return HttpResponse(
    #                 "no")
    #     else:
    #         return HttpResponse(
    #                 "yes")



class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Income
    form_class = IncomeForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Edytuj przychód'}

    # def clean_value(self):
    #     data = Outcome.objects.filter(id=self.id)
    #     print(data)
    #     return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        old_income_value = Income.objects.filter(id=self.object.id).aggregate(total=Sum('value'))['total']
        old_income_balance = Income.objects.filter(id=self.object.id).values('balance_id')[0]['balance_id']
        print(old_income_balance)
        # print(old_income_value)
        self.object.save()
        # print(self.object.value)
        # print(self.object.balance.id)
        balance = Balance.objects.filter(id=self.object.balance.id)
        balance_value = balance.aggregate(total=Sum('value'))['total']
        value_to_substract = self.object.value - old_income_value
        print(value_to_substract)

        if old_income_balance != self.object.balance.id:
            old_balance = Balance.objects.filter(id = old_income_balance)
            old_balance_value = old_balance.aggregate(total=Sum('value'))['total']
            old_balance_value -= old_income_value
            old_balance.update(value = old_balance_value)
            value_to_substract = self.object.value

        print(value_to_substract)
        balance_value += value_to_substract
        # print(value_to_substract)
        balance.update(value = balance_value)
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{self.object.comment} added."
                    })
                })

def delete_income(request, part_id=None):
    income = Income.objects.filter(id=part_id)
    income1 = income.get()
    income_value = income.aggregate(total=Sum('value'))['total']
    balance = Balance.objects.filter(id=income1.balance.id)
    balance_value = balance.aggregate(total=Sum('value'))['total']

    if request.method == "POST":
        income.delete()
        balance_value -= income_value
        balance.update(value = balance_value)
        return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "movieListChanged": None,
                        })
                    })
    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model': 'przychód','model_name':income[0].get_type_display, 'model_value':income[0].value, 'model_date': income[0].date})

@login_required(login_url='accounts:login')
def income_list(request):
    return render(request, 'finances/outcome_list.html', context={'list_what': 'Przychody'})


def get_last_date_of_month(year, month):
    """Return the last date of the month.
    
    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """
    last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
    return last_date.strftime("%Y-%m-%d")





def get_summary_data(request):
    today = date.today()
    number_of_days_in_actual_month = int(get_last_date_of_month(today.year, today.month)[-2:])
    # print(number_of_days_in_actual_month + 2)
    # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
    # if not last_balance:
    #     return JsonResponse({'error': 'No current balance has been recorded. Please add at least one current balance record.'})
        
    start_month = date.today().replace(day=1)
    end_month = get_last_date_of_month(today.year, today.month)
    
    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    prev_start_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
    # print(previous_start_month)
    # print(last_day_of_prev_month)

    # Initialise totals with sums of non repetitive incomes and outcomes
    total_balance = Balance.objects\
        .filter(user=request.user, type=1).aggregate(total=Sum('value'))['total']
    total_balance = 0 if total_balance is None else total_balance
    total_savings = Balance.objects\
        .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
    total_savings = 0 if total_savings is None else total_savings
    total_income = Income.objects\
        .filter(user=request.user, date__gte=start_month, date__lte=end_month)\
        .aggregate(total=Sum('value'))['total']
    total_income = 0 if total_income is None else total_income
    today_total_income = Income.objects\
        .filter(user=request.user, date=today)\
        .aggregate(total=Sum('value'))['total']
    today_total_income = 0 if today_total_income is None else today_total_income
    total_outcome = Outcome.objects\
        .filter(user=request.user, date__gte=start_month, date__lte=end_month)\
        .aggregate(total=Sum('value'))['total']
    total_outcome = 0 if total_outcome is None else total_outcome
    today_total_outcome = Outcome.objects\
        .filter(user=request.user, date=today)\
        .aggregate(total=Sum('value'))['total']
    today_total_outcome = 0 if today_total_outcome is None else today_total_outcome
    average_incomes_per_day = round(total_income/number_of_days_in_actual_month, 2)
    average_outcomes_per_day = round(total_outcome/number_of_days_in_actual_month, 2)

    # Savings
    total_saving_balance = Balance.objects\
        .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
    total_saving_balance = 0 if total_saving_balance is None else total_saving_balance
    last_total_balance = Balance.objects\
        .filter(user=request.user, type=2, date__gte=prev_start_month, date__lte=last_day_of_prev_month).aggregate(total=Sum('value'))['total']
    last_total_balance = 0 if last_total_balance is None else last_total_balance
    savings = total_saving_balance - last_total_balance

    # Last 5 outcomes
    last_five_outcomes_model = Outcome.objects.filter(user=request.user)[:5]
    last_five_outcomes = []
    for outcome in last_five_outcomes_model:
        last_five_outcomes.append({'id': outcome.id, 'type': outcome.get_type_display(), 'date': outcome.date, 'value': str(outcome.value).replace('.', ',')})
    print(last_five_outcomes)

    # Last 5 incomes
    last_five_incomes_model = Income.objects.filter(user=request.user)[:5]
    last_five_incomes = []
    for income in last_five_incomes_model:
        last_five_incomes.append({'id': income.id, 'type': income.get_type_display(), 'date': income.date, 'value': str(income.value).replace('.', ',')})
    print(last_five_incomes)


    translation.activate('pl')
    actual_month = date_format(today, 'F')

    # end_date = get_last_date_of_month(today.year, today.month)

    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()

    print("Actual month")
    print(get_last_date_of_month(today.year, today.month)[-2:])
    
    
    # total_outcome = Outcome.objects\
    #     .filter(user=request.user, date__gte=last_balance.date, date__lte=today, repetitive=False)\
    #     .aggregate(total=Sum('value'))['total']
    # total_outcome = 0 if total_outcome is None else total_outcome

    # incomes = Income.objects.filter(user=request.user, date__gte=last_balance.date, repetitive=False)
    # rep_incomes = Income.objects.filter(user=request.user, repetitive=True)
    # outcomes = Outcome.objects.filter(user=request.user, date__gte=last_balance.date, repetitive=False)
    # rep_outcomes = Outcome.objects.filter(user=request.user, repetitive=True)

    # Updated total with repetitive
    # for income in Income.objects.filter(user=request.user, repetitive=True):
    #     total_income += calculate_repetitive_total(income, last_balance.date, today)
    # for outcome in Outcome.objects.filter(user=request.user, repetitive=True):
    #     total_outcome += calculate_repetitive_total(outcome, last_balance.date, today)

    # context = {
    #     'last_balance': last_balance,
    #     'estimated_balance': last_balance.value + total_income - total_outcome,
    #     'total_income': total_income,
    #     'total_outcome': total_outcome
    # }

    # return render(request, 'my_finances/current_finances.html', context=context)

    return JsonResponse({
        'total_balance': str(total_balance).replace('.', ','),
        'total_savings': str(total_savings).replace('.', ','),
        'total_income': str(total_income).replace('.', ','),
        'total_outcome': str(total_outcome).replace('.', ','),
        'today_total_income': str(today_total_income).replace('.', ','),
        'today_total_outcome': str(today_total_outcome).replace('.', ','),
        'actual_month': actual_month,
        'savings': savings,
        'last_five_outcomes': last_five_outcomes,
        'last_five_incomes': last_five_incomes,
        'average_incomes_per_day': str(average_incomes_per_day).replace('.', ','),
        'average_outcomes_per_day': str(average_outcomes_per_day).replace('.', ','),
        'user_currency': user_currency,
    })

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def get_statistics_data(request):
    today = date.today()
    number_of_days_in_actual_month = int(get_last_date_of_month(today.year, today.month)[-2:])
    # print(number_of_days_in_actual_month + 2)
    # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
    # if not last_balance:
    #     return JsonResponse({'error': 'No current balance has been recorded. Please add at least one current balance record.'})
        
    start_month = date(today.year-1, 1, 1)
    end_month = date(today.year-1, 12, 31)

    print("************** uwaga statistics data ***")
    print(start_month)
    print(end_month)

    days_of_previous_year = 366 if calendar.isleap(today.year) else 365
    days_of_current_year = 366 if calendar.isleap(today.year) else 365
    print(days_of_previous_year)
    
    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    prev_start_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
    # print(previous_start_month)
    # print(last_day_of_prev_month)

    # Savings
    total_saving_balance = Balance.objects\
        .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
    total_saving_balance = 0 if total_saving_balance is None else total_saving_balance
    last_total_balance = Balance.objects\
        .filter(user=request.user, type=2, date__gte=prev_start_month, date__lte=last_day_of_prev_month).aggregate(total=Sum('value'))['total']
    last_total_balance = 0 if last_total_balance is None else last_total_balance
    savings = total_saving_balance - last_total_balance

    # Last 5 outcomes
    last_five_outcomes_model = Outcome.objects.filter(user=request.user)[:5]
    last_five_outcomes = []
    for outcome in last_five_outcomes_model:
        last_five_outcomes.append({'id': outcome.id, 'type': outcome.get_type_display(), 'date': outcome.date, 'value': str(outcome.value).replace('.', ',')})
    print(last_five_outcomes)

    # Last 5 incomes
    last_five_incomes_model = Income.objects.filter(user=request.user)[:5]
    last_five_incomes = []
    for income in last_five_incomes_model:
        last_five_incomes.append({'id': income.id, 'type': income.get_type_display(), 'date': income.date, 'value': str(income.value).replace('.', ',')})
    print(last_five_incomes)


    translation.activate('pl')
    actual_month = date_format(today, 'F')

    # end_date = get_last_date_of_month(today.year, today.month)

    print("Actual month")
    print(get_last_date_of_month(today.year, today.month)[-2:])
    
    
    # total_outcome = Outcome.objects\
    #     .filter(user=request.user, date__gte=last_balance.date, date__lte=today, repetitive=False)\
    #     .aggregate(total=Sum('value'))['total']
    # total_outcome = 0 if total_outcome is None else total_outcome

    # incomes = Income.objects.filter(user=request.user, date__gte=last_balance.date, repetitive=False)
    # rep_incomes = Income.objects.filter(user=request.user, repetitive=True)
    # outcomes = Outcome.objects.filter(user=request.user, date__gte=last_balance.date, repetitive=False)
    # rep_outcomes = Outcome.objects.filter(user=request.user, repetitive=True)

    # Updated total with repetitive
    # for income in Income.objects.filter(user=request.user, repetitive=True):
    #     total_income += calculate_repetitive_total(income, last_balance.date, today)
    # for outcome in Outcome.objects.filter(user=request.user, repetitive=True):
    #     total_outcome += calculate_repetitive_total(outcome, last_balance.date, today)

    # context = {
    #     'last_balance': last_balance,
    #     'estimated_balance': last_balance.value + total_income - total_outcome,
    #     'total_income': total_income,
    #     'total_outcome': total_outcome
    # }

    # return render(request, 'my_finances/current_finances.html', context=context)

    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()

    # at least one object satisfying query exists

    first_income_date = Income.objects.filter(user=request.user).order_by('date').first().date
    first_outcome_date = Outcome.objects.filter(user=request.user).order_by('date').first().date
    first_income_outcome_date = min(first_income_date, first_outcome_date)
    print(f"pierwsza daata to: {first_income_outcome_date}")
    # last_income_date = today

    number_of_days_in_last_income_month = int(get_last_date_of_month(today.year, today.month)[-2:])
    # # first_income_date = 
    print(first_income_date)
    print(today)
    # month_diference = 12
    monday1 = (first_income_outcome_date - timedelta(days=first_income_outcome_date.weekday()))
    monday2 = (today - timedelta(days=today.weekday()))
    date_delta = relativedelta.relativedelta(today, first_income_outcome_date)
    days_difference = (today - first_income_outcome_date).days
    weeks_difference = Decimal((monday2 - monday1).days / 7)
    months_difference = Decimal(days_difference / 30)
    if months_difference < 1:
        months_difference = 0
    years_difference = Decimal(days_difference / 365)
    if years_difference < 1:
        years_difference = 0
    # print(f"Roznica w latach: {years_difference}")
    # print(f'Pierwszy income - {first_income_date}')
    # print(f"Roznica w miesiacach: {months_difference}")
    # print(f"Roznica w dniach: {first_income_outcome_date}")
    # print(f"Roznica w tyg: {first_income_outcome_date}")

    # if first_income_date.year > today.year - 1:
    #     if first_income_date.year == today.year:
    #         print("zgodne")
    #         month_diference = today.month - first_income_date.month + 1
    #         if first_income_date.day != 1:
    #             print("rozny od 1")
    #             month_diference -= 1
    #         if today.day != number_of_days_in_last_income_month:
    #             print(f"last rowniez rozny od {number_of_days_in_last_income_month}")
    #             month_diference -= 1

    #         print(month_diference)


# no object satisfying query exists

# print(diff_month(today, first_income_date))



# print(f"Roznica month: {res_months}")

    # print(diff_month(datetime(2010,10,13), datetime(2008,10,1)))
    # print(list(rrule.rrule(rrule.MONTHLY, dtstart=first_income_date, until=today)))

    # Initialise totals with sums of non repetitive incomes and outcomes
    total_balance = Balance.objects\
        .filter(user=request.user, type=1).aggregate(total=Sum('value'))['total']
    total_balance = 0 if total_balance is None else total_balance
    total_savings = Balance.objects\
        .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
    total_savings = 0 if total_savings is None else total_savings
    total_income = Income.objects\
        .filter(user=request.user)\
        .aggregate(total=Sum('value'))['total']
    total_income = 0 if total_income is None else total_income
    total_outcome = Outcome.objects\
        .filter(user=request.user)\
        .aggregate(total=Sum('value'))['total']
    total_outcome = 0 if total_outcome is None else total_outcome


    average_incomes_per_day = total_income if days_difference == 0 else round(total_income/days_difference, 2)
    average_outcomes_per_day = total_outcome if days_difference == 0 else round(total_outcome/days_difference, 2)

    average_incomes_per_week = total_income if weeks_difference == 0 else round(total_income/weeks_difference, 2)
    average_outcomes_per_week = total_outcome if weeks_difference == 0 else round(total_outcome/weeks_difference, 2)

    average_incomes_per_month = total_income if months_difference == 0 else round(total_income/months_difference, 2)
    average_outcomes_per_month = total_outcome if months_difference == 0 else round(total_outcome/months_difference, 2)

    average_incomes_per_year = total_income if years_difference == 0 else round(total_income/years_difference, 2)
    average_outcomes_per_year = total_outcome if years_difference == 0 else round(total_outcome/years_difference, 2)

    return JsonResponse({
        'total_balance': str(total_balance).replace('.', ','),
        'total_savings': str(total_savings).replace('.', ','),
        'total_income': str(total_income).replace('.', ','),
        'total_outcome': str(total_outcome).replace('.', ','),
        'actual_month': actual_month,
        'savings': savings,
        'years_difference': years_difference,
        'last_five_outcomes': last_five_outcomes,
        'last_five_incomes': last_five_incomes,
        'average_incomes_per_day': str(average_incomes_per_day).replace('.', ','),
        'average_outcomes_per_day': str(average_outcomes_per_day).replace('.', ','),
        'average_incomes_per_week': str(average_incomes_per_week).replace('.', ','),
        'average_outcomes_per_week': str(average_outcomes_per_week).replace('.', ','),
        'average_incomes_per_month': str(average_incomes_per_month).replace('.', ','),
        'average_outcomes_per_month': str(average_outcomes_per_month).replace('.', ','),
        'average_incomes_per_year': str(average_incomes_per_year).replace('.', ','),
        'average_outcomes_per_year': str(average_outcomes_per_year).replace('.', ','),
        'user_currency': user_currency,
    })

    # else:
    #     return JsonResponse({
    #         'actual_month': actual_month,
    #         'last_five_outcomes': last_five_outcomes,
    #         'last_five_incomes': last_five_incomes,
    #         'income_information': 'Nie wprowadzono jeszcze żadnych przychodów',
    #         'outcome_information': 'Nie wprowadzono jeszcze żadnych wydatków',
    #         'average_incomes_per_month': '',
    #         'average_outcomes_per_month': '',
    #         'data_exist': False,
    #         'user_currency': user_currency,
    #     })

    




# def get_savings_data(request):
#     today = date.today()
#     # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
#     # if not last_balance:
#     #     return JsonResponse({'error': 'No current balance has been recorded. Please add at least one current balance record.'})
        
#     start_month = date.today().replace(day=1)
#     end_month = get_last_date_of_month(today.year, today.month)
    
#     last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
#     prev_start_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
#     # print(previous_start_month)
#     # print(last_day_of_prev_month)

#     # Initialise totals with sums of non repetitive incomes and outcomes
#     total_savings_balance = Balance.objects\
#         .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
#     total_savings_balance = 0 if total_savings_balance is None else total_savings_balance
#     # total_income = Income.objects\
#     #     .filter(user=request.user, date__gte=start_month, date__lte=end_month)\
#     #     .aggregate(total=Sum('value'))['total']
#     # total_income = 0 if total_income is None else total_income
#     # total_outcome = Outcome.objects\
#     #     .filter(user=request.user, date__gte=start_month, date__lte=end_month)\
#     #     .aggregate(total=Sum('value'))['total']
#     # total_outcome = 0 if total_outcome is None else total_outcome

#     # Savings
#     # total_saving_balance = Balance.objects\
#     #     .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
#     # total_saving_balance = 0 if total_saving_balance is None else total_saving_balance
#     # last_total_balance = Balance.objects\
#     #     .filter(user=request.user, type=2, date__gte=prev_start_month, date__lte=last_day_of_prev_month).aggregate(total=Sum('value'))['total']
#     # last_total_balance = 0 if last_total_balance is None else last_total_balance
#     # savings = total_saving_balance - last_total_balance

#     # Last 5 outcomes
#     # last_five_outcomes_model = Outcome.objects.filter(user=request.user)[:5]
#     # last_five_outcomes = []
#     # for outcome in last_five_outcomes_model:
#     #     last_five_outcomes.append({'id': outcome.id, 'type': outcome.get_type_display(), 'date': outcome.date, 'value': outcome.value})
#     # print(last_five_outcomes)

#     # Last 5 incomes
#     # last_five_incomes_model = Income.objects.filter(user=request.user)[:5]
#     # last_five_incomes = []
#     # for income in last_five_incomes_model:
#     #     last_five_incomes.append({'id': income.id, 'type': income.get_type_display(), 'date': income.date, 'value': income.value})
#     # print(last_five_incomes)

#     translation.activate('pl')
#     actual_month = date_format(date.today(), 'F')
    
    
#     # total_outcome = Outcome.objects\
#     #     .filter(user=request.user, date__gte=last_balance.date, date__lte=today, repetitive=False)\
#     #     .aggregate(total=Sum('value'))['total']
#     # total_outcome = 0 if total_outcome is None else total_outcome

#     # incomes = Income.objects.filter(user=request.user, date__gte=last_balance.date, repetitive=False)
#     # rep_incomes = Income.objects.filter(user=request.user, repetitive=True)
#     # outcomes = Outcome.objects.filter(user=request.user, date__gte=last_balance.date, repetitive=False)
#     # rep_outcomes = Outcome.objects.filter(user=request.user, repetitive=True)

#     # Updated total with repetitive
#     # for income in Income.objects.filter(user=request.user, repetitive=True):
#     #     total_income += calculate_repetitive_total(income, last_balance.date, today)
#     # for outcome in Outcome.objects.filter(user=request.user, repetitive=True):
#     #     total_outcome += calculate_repetitive_total(outcome, last_balance.date, today)

#     # context = {
#     #     'last_balance': last_balance,
#     #     'estimated_balance': last_balance.value + total_income - total_outcome,
#     #     'total_income': total_income,
#     #     'total_outcome': total_outcome
#     # }

#     # return render(request, 'my_finances/current_finances.html', context=context)

#     return JsonResponse({
#         # 'total_balance': str(total_balance).replace('.', ','),
#         # 'total_income': str(total_income).replace('.', ','),
#         # 'total_outcome': str(total_outcome).replace('.', ','),
#         'actual_month': actual_month,
#         # 'savings': savings,
#         # 'last_five_outcomes': last_five_outcomes,
#         # 'last_five_incomes': last_five_incomes,
#         'total_savings_balance': str(total_savings_balance).replace('.', ','),
#     })


# def get_balance_chart(request):
#     all_sleep = Balance.objects.filter(user=request.user, type=1).order_by('date')

#     date_list = [sleep_date['date'] for sleep_date in Balance.objects.filter(user=request.user).order_by('date').values('date').distinct()]

#     today = datetime.now()    
#     print(today.date())
#     n_days_ago = today - timedelta(days=14)

#     date_last14 = []

#     for i in range(14, -1 ,-1):
#         n_days_ago = today - timedelta(days=i)
#         date_last14.append(n_days_ago.date())

#     sum_value_at_date = []
    

#     for sleep_date in date_last14:
#         activities_tot = Balance.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=sleep_date)))['s']
#         if activities_tot is None:
#             sum_value_at_date.append(0)
#         else:
#             sum_value_at_date.append(activities_tot)

#     sum = 0
#     items = 0
#     for item in sum_value_at_date:
#         if item != 0:
#             sum += item
#             items += 1

#     if items == 0:
#         average = 0
#     else:
#         average = sum/items
#     print(average)

#     print(sum_value_at_date)

#     first_date_of_14_days = date_last14[0]
#     last_date_of_14_days = date_last14[-1]

#     # context = {
        
#     # }

#     return JsonResponse({
#         # 'all_sleep': all_sleep,
#         'date_last14': date_last14,
#         'data': sum_value_at_date,
#         'first_date_of_14_days': first_date_of_14_days,
#         'last_date_of_14_days': last_date_of_14_days,
#         'sleep_avg': average
#     })


def get_year_chart_custom(request):
    # balance_type = request.GET.get('balance_type')
    # if balance_type not in ['current', 'savings']:
    #     return JsonResponse({'error': 'Please specify balanse_type parameter to be either "current" or "savings"'})

    # today = date.today()
    # beginning_of_year = date(today.year, 1, 1)
    # end_of_year = date(today.year, 12, 28)
    # # Try to get last balance check before the beginning of this year
    # balance = Balance.objects.filter(user=request.user, type=1 if balance_type == 'current' else 2, date__lte=beginning_of_year) \
    #     .order_by('-date').first()
    # if balance is None:
    #     # If there's no balance check before the year - get this first one of this year
    #     balance = Balance.objects.filter(user=request.user, type=1 if balance_type == 'current' else 2).order_by('date').first()
    #     if balance is None:
    #         return JsonResponse({'error': 'No current balance has been recorded. '
    #                                       'Please add at least one current balance record.'})

    all_sleep = Balance.objects.filter(user=request.user).order_by('date')

    all_incomes = Income.objects.filter(user=request.user)

    all_outcomes = Outcome.objects.filter(user=request.user)

    context_label = Account.objects.get(user_id=request.user.id).get_currency_display()

    # Balance.objects
    #     .annotate(month=TruncMonth('created'))  # Truncate to month and add to select list
    #     .values('month')                          # Group By month
    #     .annotate(c=Count('id'))                  # Select the count of the grouping
    #     .values('month', 'c')                     # (might be redundant, haven't tested) select month and count 

    # date_list = [sleep_date['date'] for sleep_date in Balance.objects.filter(user=request.user).order_by('date').values('date').distinct()]

    N = 12 * 30

    today = datetime.now()    
    #print(today.date())
    n_days_ago = today - timedelta(days=N)

    date_last_time = []

    for i in range(N, -1 ,-1):
        n_days_ago = today - timedelta(days=i)
        date_last_time.append(n_days_ago.date())

    sum_value_at_date = []
    

    for sleep_date in date_last_time:
        activities_tot = Balance.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=sleep_date)))['s']
        sum_value_at_date.append(activities_tot)

    daty = []

    month_labels = [
        "Styczeń",
        "Luty",
        "Marzec",
        "Kwiecień",
        "Maj",
        "Czerwiec",
        "Lipiec",
        "Sierpień",
        "Wrzesień",
        "Październik",
        "Listopad",
        "Grudzień"
    ]


    total_income_monthly_sum = []
    total_outcome_monthly_sum = []

    month_days_30 = [4,6,9,11]

    for i in range(1,12):
        start_date = date(today.year, i, 1)
        if i == 2:
            end_date = date(today.year, i, 28)
        elif i in month_days_30:
            end_date = date(today.year, i, 30)

        else:
            end_date = date(today.year, i, 31)

        total_income_monthly = Income.objects\
            .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
            .aggregate(total=Sum('value'))['total']

        total_outcome_monthly = Outcome.objects\
            .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
            .aggregate(total=Sum('value'))['total']

        total_income_monthly_sum.append(total_income_monthly)
        total_outcome_monthly_sum.append(total_outcome_monthly)

        daty.append(start_date)
        daty.append(end_date)

    # print(daty)
    # print(total_income_monthly_sum)
    # print(total_outcome_monthly_sum)
        

    # januar_start_date = date(today.year, 1, 1)
    # januar_end_date = date(today.year, 1, 31)

    # januar_start_date = date(today.year, 1, 1)
    # januar_end_date = date(today.year, 1, 31)

    # januar_start_date = date(today.year, 1, 1)
    # januar_end_date = date(today.year, 1, 31)

    # total_year_outcomes = Outcome.objects\
    #     .filter(user=request.user, date__gte=date(today.year, 1, 1), date__lte=date(today.year, 12, 31))\
    #     .aggregate(total=Sum('value'))['total']

    # average_monthly_outcomes = round((total_year_outcomes/12), 2)

    
    # print(total_income_januar)

    print([v for v in
       Income.objects.annotate(month=TruncMonth('date'))
                      .values('month')
                      .annotate(total=Count('value'))
                      .values('month', 'total')
       ])

    sum = 0
    items = 0
    # for item in sum_value_at_date:
    #     if item != 0:
    #         sum += item
    #         items += 1

    if items == 0:
        average = 0
    else:
        average = sum/items
    print(average)

    print(sum_value_at_date)

    first_date_of_14_days = date_last_time[0]
    last_date_of_14_days = date_last_time[-1]

    return JsonResponse({
        # 'all_sleep': all_sleep,
        'date_last14': date_last_time,
        'month_labels': month_labels,
        'data': sum_value_at_date,
        'first_date_of_14_days': first_date_of_14_days,
        'last_date_of_14_days': last_date_of_14_days,
        'total_income_monthly_sum': total_income_monthly_sum,
        'total_outcome_monthly_sum': total_outcome_monthly_sum,
        'sleep_avg': average,
        'context_label': context_label
    })




# def get_year_chart(request):
#     balance_type = request.GET.get('balance_type')
#     if balance_type not in ['current', 'savings']:
#         return JsonResponse({'error': 'Please specify balanse_type parameter to be either "current" or "savings"'})

#     today = date.today()
#     beginning_of_year = date(today.year, 1, 1)
#     end_of_year = date(today.year, 12, 28)
#     # Try to get last balance check before the beginning of this year
#     balance = Balance.objects.filter(user=request.user, type=1 if balance_type == 'current' else 2, date__lte=beginning_of_year) \
#         .order_by('-date').first()
#     if balance is None:
#         # If there's no balance check before the year - get this first one of this year
#         balance = Balance.objects.filter(user=request.user, type=1 if balance_type == 'current' else 2).order_by('date').first()
#         if balance is None:
#             return JsonResponse({'error': 'No current balance has been recorded. '
#                                           'Please add at least one current balance record.'})

#     # Assuming we found balance - we start calculating from there
#     balance_checks = {}
#     income_per_day = {}
#     outcome_per_day = {}

#     for b in Balance.objects.filter(user=request.user, type=1 if balance_type == 'current' else 2, date__gte=balance.date):
#         balance_checks[str(b.date)] = b.value

#     if balance_type == 'current':
#         for i in Income.objects.filter(user=request.user, date__gte=balance.date):
#             income_per_day[str(i.date)] = i.value if str(i.date) not in income_per_day \
#                 else income_per_day[str(i.date)] + i.value
#         for o in Outcome.objects.filter(user=request.user, date__gte=balance.date):
#             outcome_per_day[str(o.date)] = o.value if str(o.date) not in outcome_per_day \
#                 else outcome_per_day[str(o.date)] + o.value


#     else:
#         # If balance_type is saving, we want to only look at incomes and outcomes of type SAVINGS
#         # Also, income of type SAVING will act like an outcome for saving balance and vice versa
#         for i in Income.objects.filter(user=request.user, date__gte=balance.date, type=5):
#             outcome_per_day[str(i.date)] = i.value if str(i.date) not in outcome_per_day \
#                 else outcome_per_day[str(i.date)] + i.value
#         for o in Outcome.objects.filter(user=request.user, date__gte=balance.date, type=10):
#             income_per_day[str(o.date)] = o.value if str(o.date) not in income_per_day \
#                 else income_per_day[str(o.date)] + o.value




#     labels = []
#     data_estimated = []
#     data_balance_check = []
#     data_today = []
#     date_marker = balance.date
#     balance_on_marker_date = balance.value

#     if date_marker > beginning_of_year:
#         fill_date_marker = date(today.year, 1, 1)
#         while fill_date_marker < date_marker:
#             labels.append(str(fill_date_marker))
#             data_estimated.append(None)
#             data_balance_check.append(None)
#             data_today.append(None)
#             fill_date_marker += timedelta(days=1)
#     else:
#         while date_marker < beginning_of_year:
#             balance_on_marker_date += income_per_day.get(str(date_marker), 0)
#             balance_on_marker_date -= outcome_per_day.get(str(date_marker), 0)
#             date_marker += timedelta(days=1)

#     # Calculate and prepare balance per day for this year
#     while date_marker <= end_of_year:
#         labels.append(str(date_marker))
#         if str(date_marker) in balance_checks:
#             balance_on_marker_date = balance_checks[str(date_marker)]
#             data_balance_check.append(balance_checks[str(date_marker)])
#         else:
#             balance_on_marker_date += income_per_day.get(str(date_marker), 0)
#             balance_on_marker_date -= outcome_per_day.get(str(date_marker), 0)
#             data_balance_check.append(None)
#         data_estimated.append(balance_on_marker_date)
#         if date_marker == today:
#             data_today.append(balance_on_marker_date)
#         else:
#             data_today.append(None)
#         date_marker += timedelta(days=1)
#     return JsonResponse({'labels': labels, 'data_estimated': data_estimated, 'data_balance_check': data_balance_check,
#                          'data_today': data_today})


def get_income_or_outcome_by_type(request):
    get_what = request.GET.get('get_what')
    summary_type = request.GET.get('summary_type')
    view_type = request.GET.get('view_type')
    if get_what is None or get_what not in ['income', 'outcome']:
        return JsonResponse({'error': 'Please specify get_what parameter to be either "income or "outcome'})
    if get_what == 'income':
        obj = Income
        obj_types = Income.ITypes
    else:
        obj = Outcome
        obj_types = Outcome.OTypes

    today = date.today()

    month_days_30 = [4,6,9,11]

    # for i in range(1,12):
    #     start_date = date(today.year, i, 1)
    #     if i == 2:
    #         end_date = date(today.year, i, 28)
    #     elif i in month_days_30:
    #         end_date = date(today.year, i, 30)

    #     else:
    #         end_date = date(today.year, i, 31)

    if summary_type == 'mon1':
        # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
        # if not last_balance:
        #     return JsonResponse({'error': 'No current balance has been recorded. '
        #                         'Please add at least one current balance record. '})
        
        # start_date = 
        # end_date = today
        start_date = date.today().replace(day=1)
        end_date = get_last_date_of_month(today.year, today.month)
        print("Miesiace")
        print(start_date)
        print(end_date)
        print("Koniec")
        

    elif summary_type == 'week':
        start_date = date.today() - timedelta(days=7)

        end_date = date.today()
        print("Miesiace")
        print(start_date)
        print(end_date)
        print("Koniec")

    elif summary_type == 'mon3':
        start_date = date.today().replace(day=1) - timedelta(days=60)
        start_date = start_date.replace(day=1)

        end_date = get_last_date_of_month(today.year, today.month)
        print("Miesiace")
        print(start_date)
        print(end_date)
        print("Koniec")

    elif summary_type == 'mon6':
        start_date = date.today().replace(day=1) - timedelta(days=140)
        start_date = start_date.replace(day=1)

        end_date = get_last_date_of_month(today.year, today.month)
        print("Miesiace")
        print(start_date)
        print(end_date)
        print("Koniec")
    
    elif summary_type == 'year1':
        start_date = date(today.year, 1, 1)

        end_date = date(today.year, 12, 31)
        print("Miesiace")
        print(start_date)
        print(end_date)
        print("Koniec")
    
    elif summary_type == 'all':
        last_object = obj.objects.filter(user=request.user).order_by('-date').first()
        first_object = obj.objects.filter(user=request.user).order_by('-date').last()
        start_date = first_object.date

        end_date = last_object.date
        print("Miesiace")
        print(start_date)
        print(end_date)
        print("Koniec")

    else:
        return JsonResponse({'error': 'Please specify summary_type parameter to be either current_period or year_overview'})
    
    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()

    labels = []
    data = []
    context_label = ''
    if view_type == 'amount':
        for obj_type in obj_types.choices:
            labels.append(obj_type[1])
            total = obj.objects.filter(user=request.user, type=obj_type[0], date__gte=start_date,
                date__lte=end_date).aggregate(total=Sum('value'))['total']
            total = 0 if total is None else total

            data.append(total)
        context_label = user_currency
    
    elif view_type == 'percentage':
        total_all = obj.objects.filter(user=request.user, date__gte=start_date,
                date__lte=end_date).aggregate(total=Sum('value'))['total']
        for obj_type in obj_types.choices:
            labels.append(obj_type[1])
            total = obj.objects.filter(user=request.user, type=obj_type[0], date__gte=start_date,
                date__lte=end_date).aggregate(total=Sum('value'))['total']
            total = 0 if total is None else total

            data.append(round((total/total_all)*100, 2))
        context_label = '%'

    else:
        return JsonResponse({'error': 'Please specify view_type parameter to be either amount or percentage'})

    return JsonResponse({'labels': labels, 'data': data, 'context_label': context_label})


# def get_progressbar_data(request):
#     get_what = request.GET.get('get_what')
#     summary_type = request.GET.get('summary_type')
#     if get_what is None or get_what not in ['income', 'outcome']:
#         return JsonResponse({'error': 'Please specify get_what parameter to be either "income or "outcome'})
#     if get_what == 'income':
#         obj = Income
#         obj_types = Income.ITypes
#     else:
#         obj = Outcome
#         obj_types = Outcome.OTypes

#     today = date.today()

#     month_days_30 = [4,6,9,11]

#     # for i in range(1,12):
#     #     start_date = date(today.year, i, 1)
#     #     if i == 2:
#     #         end_date = date(today.year, i, 28)
#     #     elif i in month_days_30:
#     #         end_date = date(today.year, i, 30)

#     #     else:
#     #         end_date = date(today.year, i, 31)

#     if summary_type == 'mon1':
#         # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
#         # if not last_balance:
#         #     return JsonResponse({'error': 'No current balance has been recorded. '
#         #                         'Please add at least one current balance record. '})
        
#         # start_date = 
#         # end_date = today
#         start_date = date.today().replace(day=1)
#         end_date = get_last_date_of_month(today.year, today.month)
#         print("Miesiace")
#         print(start_date)
#         print(end_date)
#         print("Koniec")
        

#     elif summary_type == 'week':
#         start_date = date.today() - timedelta(days=7)

#         end_date = date.today()
#         print("Miesiace")
#         print(start_date)
#         print(end_date)
#         print("Koniec")

#     elif summary_type == 'mon3':
#         start_date = date.today().replace(day=1) - timedelta(days=60)
#         start_date = start_date.replace(day=1)

#         end_date = get_last_date_of_month(today.year, today.month)
#         print("Miesiace")
#         print(start_date)
#         print(end_date)
#         print("Koniec")

#     elif summary_type == 'mon6':
#         start_date = date.today().replace(day=1) - timedelta(days=140)
#         start_date = start_date.replace(day=1)

#         end_date = get_last_date_of_month(today.year, today.month)
#         print("Miesiace")
#         print(start_date)
#         print(end_date)
#         print("Koniec")
    
#     elif summary_type == 'year1':
#         start_date = date(today.year, 1, 1)

#         end_date = date(today.year, 12, 31)
#         print("Miesiace")
#         print(start_date)
#         print(end_date)
#         print("Koniec")
    
#     elif summary_type == 'all':
#         last_object = obj.objects.filter(user=request.user).order_by('-date').first()
#         first_object = obj.objects.filter(user=request.user).order_by('-date').last()
#         start_date = first_object.date

#         end_date = last_object.date
#         print("Miesiace")
#         print(start_date)
#         print(end_date)
#         print("Koniec")

#     else:
#         return JsonResponse({'error': 'Please specify summary_type parameter to be either current_period or year_overview'})
    
#     labels = []
#     data = []
#     progress_bar_data = []

#     total_all_objects = obj.objects.filter(user=request.user, date__gte=start_date,
#         date__lte=end_date).aggregate(total=Sum('value'))['total']

#     last_five_outcomes = []
#     # id = 0
    
#     for obj_type in obj_types.choices:
#         labels.append(obj_type[1])
#         total = obj.objects.filter(user=request.user, type=obj_type[0], date__gte=start_date,
#             date__lte=end_date).aggregate(total=Sum('value'))['total']
#         total = 0 if total is None else total

#         progress = total/total_all_objects

#         last_five_outcomes.append({'type': obj_type[1], 'value': total, 'progress': progress})


#         data.append(total)
#         progress_bar_data.append(progress)

#         # id += 1

#     last_five_outcomes.sort(key=lambda item: item['value'], reverse=True)    

#     return JsonResponse({'labels': labels, 'data': data, 'total_all_objects': total_all_objects, 'progress_bar_data': progress_bar_data, 'last_five_outcomes':last_five_outcomes})


# W tej funkcji trzeba w zaleznosci od summary type pododawac do wykresy wydatki i przychdy
def get_income_or_outcome_bar_chart(request):
    get_what = request.GET.get('get_what')
    summary_type = request.GET.get('summary_type')
    if get_what is None or get_what not in ['income', 'outcome']:
        return JsonResponse({'error': 'Please specify get_what parameter to be either "income or "outcome'})
    if get_what == 'income':
        obj = Income
        obj_types = Income.ITypes
    else:
        obj = Outcome
        obj_types = Outcome.OTypes

    today = date.today()

    context_label = Account.objects.get(user_id=request.user.id).get_currency_display()

    month_days_30 = [4,6,9,11]

    labels = []
    data = []

    translation.activate('pl')


    # for i in range(1,12):
    #     start_date = date(today.year, i, 1)
    #     if i == 2:
    #         end_date = date(today.year, i, 28)
    #     elif i in month_days_30:
    #         end_date = date(today.year, i, 30)

    #     else:
    #         end_date = date(today.year, i, 31)

    if summary_type == 'mon1':
        # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
        # if not last_balance:
        #     return JsonResponse({'error': 'No current balance has been recorded. '
        #                         'Please add at least one current balance record. '})
        
        # start_date = 
        # end_date = today

        total_income_monthly_sum = []
        total_outcome_monthly_sum = []


        # all_activities_today = Activity.objects.filter(date=date.today(), user=request.user)

        # all_activities = Activity.objects.filter(user=request.user).order_by('date')

        # type_list = [activity_type['type'] for activity_type in Activity.objects.filter(user=request.user).values('type')]

        # print(type_list)

        # date_list = [activity_date['date'] for activity_date in Activity.objects.filter(user=request.user).values('date').order_by('date').distinct()]

        today = datetime.now()

        # labels = []

        month_days_30 = [4,6,9,11]

        if today.month in month_days_30:
            N = 30
        else:
            N = 31

        start_date = date(today.year, today.month, 1)
        end_date = get_last_date_of_month(today.year, today.month)

        print(start_date)
        print(end_date)
        print(N)


        # n_days_ago = today - timedelta(days=N)

        # labels.append(start_date)


        for i in range(1,N+1):
            print(i)
            labels.append(start_date)
            start_date += timedelta(days=1)

        print(today.month)

        #print("Daty",date_last14)

        activity_label = []

        # for activity in all_activities_today:
        #     activity_label.append(activity.type)

        for activity_date in labels:
            total = obj.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=activity_date)))['s']
            # if total is None:
            #     data.append(0)
            # else:
            data.append(total)


        # for i in range(1,12):
        #     start_date = date(today.year, i, 1)
        #     if i == 2:
        #         end_date = date(today.year, i, 28)
        #     elif i in month_days_30:
        #         end_date = date(today.year, i, 30)

        #     else:
        #         end_date = date(today.year, i, 31)

        #     total_income_monthly = Income.objects\
        #         .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
        #         .aggregate(total=Sum('value'))['total']

        #     total_outcome_monthly = Outcome.objects\
        #         .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
        #         .aggregate(total=Sum('value'))['total']

        #     total_income_monthly_sum.append(total_income_monthly)
        #     total_outcome_monthly_sum.append(total_outcome_monthly)

        #     daty.append(start_date)
        #     daty.append(end_date)

        #     print(daty)
        #     print(total_income_monthly_sum)
        #     print(total_outcome_monthly_sum)
            
        
        #     start_date = date.today().replace(day=1)
        #     end_date = get_last_date_of_month(today.year, today.month)
        #     print("Miesiace")
        #     print(start_date)
        #     print(end_date)
        #     print("Koniec")
        

    elif summary_type == 'week':
        # start_date = date.today() - timedelta(days=7)

        # end_date = date.today()
        # print("Miesiace")
        # print(start_date)
        # print(end_date)
        # print("Koniec")

        today = datetime.now()

        # labels = []

        month_days_30 = [4,6,9,11]

        # if today.month in month_days_30:
        #     N = 30
        # else:
        #     N = 31

        start_date = date.today() - timedelta(days=7)

        end_date = date.today()
        N = 8

        # start_date = date(today.year, today.month, 1)
        # end_date = get_last_date_of_month(today.year, today.month)

        print(start_date)
        print(end_date)
        print(N)

        dates = []


        # n_days_ago = today - timedelta(days=N)

        # labels.append(start_date)


        for i in range(1,N+1):
            print(i)
            dates.append(start_date)
            labels.append(f"{date_format(start_date, 'D')} ({start_date})")
            start_date += timedelta(days=1)

        print(today.month)

        #print("Daty",date_last14)

        activity_label = []

        # for activity in all_activities_today:
        #     activity_label.append(activity.type)

        for activity_date in dates:
            total = obj.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=activity_date)))['s']
            # if total is None:
            #     data.append(0)
            # else:
            data.append(total)

        

    elif summary_type == 'mon3':

        first_month_start_date = (date.today().replace(day=1) - timedelta(days=60)).replace(day=1)
        first_month_end_date = get_last_date_of_month(today.year, first_month_start_date.month)

        second_month_start_date = (first_month_start_date + timedelta(days=40)).replace(day=1)
        second_month_end_date = get_last_date_of_month(today.year, second_month_start_date.month)

        third_month_start_date = date.today().replace(day=1)
        third_month_end_date = get_last_date_of_month(today.year, today.month)

        start_dates = [first_month_start_date, second_month_start_date, third_month_start_date]
        end_dates = [first_month_end_date, second_month_end_date, third_month_end_date]

        for start_date,end_date in zip(start_dates, end_dates):
            print(f"{start_date} - {end_date}")
            labels.append(date_format(start_date, 'F'))
            total = obj.objects.filter(user=request.user, date__gte=start_date,
                date__lte=end_date).aggregate(total=Sum('value'))['total']
            data.append(total)

        # first_month = date_format(first_month_start_date, 'F')
        # second_month = date_format(second_month_start_date, 'F')
        # third_month = date_format(third_month_start_date, 'F')

        # labels1 = [first_month, second_month, third_month]


        # print(first_month)
        # print(second_month)
        # print(third_month)
        # print(labels1)




        # n_days_ago = today - timedelta(days=N)

        # labels.append(start_date)


        # for i in range(1,10+1):
        #     print(i)
        #     labels.append(first_month_start_date)
        #     first_month_start_date += timedelta(days=1)

        # print(today.month)

        #print("Daty",date_last14)


        # for activity in all_activities_today:
        #     activity_label.append(activity.type)

        # for activity_date in labels:
        #     total = obj.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=activity_date)))['s']
        #     # if total is None:
        #     #     data.append(0)
        #     # else:
        #     data.append(total)

        # month_days_30 = [4,6,9,11]


    elif summary_type == 'mon6':
        first_month_start_date = (date.today().replace(day=1) - timedelta(days=140)).replace(day=1)
        first_month_end_date = get_last_date_of_month(today.year, first_month_start_date.month)
        
        second_month_start_date = (first_month_start_date + timedelta(days=40)).replace(day=1)
        second_month_end_date = get_last_date_of_month(today.year, second_month_start_date.month)

        third_month_start_date = (second_month_start_date + timedelta(days=40)).replace(day=1)
        third_month_end_date = get_last_date_of_month(today.year, third_month_start_date.month)

        fourth_month_start_date = (third_month_start_date + timedelta(days=40)).replace(day=1)
        fourth_month_end_date = get_last_date_of_month(today.year, fourth_month_start_date.month)

        fifth_month_start_date = (fourth_month_start_date + timedelta(days=40)).replace(day=1)
        fifth_month_end_date = get_last_date_of_month(today.year, fifth_month_start_date.month)

        sixth_month_start_date = date.today().replace(day=1)
        sixth_month_end_date = get_last_date_of_month(today.year, today.month)

        start_dates = [first_month_start_date, second_month_start_date, third_month_start_date, fourth_month_start_date, fifth_month_start_date, sixth_month_start_date]
        end_dates = [first_month_end_date, second_month_end_date, third_month_end_date, fourth_month_end_date, fifth_month_end_date, sixth_month_end_date]

        for start_date,end_date in zip(start_dates, end_dates):
            print(f"{start_date} - {end_date}")
            labels.append(date_format(start_date, 'F'))
            total = obj.objects.filter(user=request.user, date__gte=start_date,
                date__lte=end_date).aggregate(total=Sum('value'))['total']
            data.append(total)

    
    elif summary_type == 'year1':

        for i in range(1,13):
            start_date = date(today.year, i, 1)
            # tutaj trzeba sprawdzic czy rok przestepny
            if i == 2:
                end_date = date(today.year, i, 28)
            elif i in month_days_30:
                end_date = date(today.year, i, 30)

            else:
                end_date = date(today.year, i, 31)

            print(f"{start_date} - {end_date}")
            labels.append(date_format(start_date, 'F'))
            total = obj.objects.filter(user=request.user, date__gte=start_date,
                date__lte=end_date).aggregate(total=Sum('value'))['total']
            data.append(total)

            # print(start_date)
            # print(end_date)

            # total_income_monthly = Income.objects\
            #     .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
            #     .aggregate(total=Sum('value'))['total']

            # total_outcome_monthly = Outcome.objects\
            #     .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
            #     .aggregate(total=Sum('value'))['total']

            # total_income_monthly_sum.append(total_income_monthly)
            # total_outcome_monthly_sum.append(total_outcome_monthly)

            # daty.append(start_date)
            # daty.append(end_date)

            # print(daty)
            # print(total_income_monthly_sum)
            # print(total_outcome_monthly_sum)
            
        
            # start_date = date.today().replace(day=1)
            # end_date = get_last_date_of_month(today.year, today.month)
            # print("Miesiace")
            # print(start_date)
            # print(end_date)
            # print("Koniec")
    
    # elif summary_type == 'all':
    #     last_object = obj.objects.filter(user=request.user).order_by('-date').first()
    #     first_object = obj.objects.filter(user=request.user).order_by('-date').last()
    #     start_date = first_object.date

    #     end_date = last_object.date
    #     print("Miesiace")
    #     print(start_date)
    #     print(end_date)
    #     print("Koniec")

    else:
        return JsonResponse({'error': 'Please specify summary_type parameter to be either current_period or year_overview'})
    
    # labels = []
    # data = []
    # for obj_type in obj_types.choices:
    #     labels.append(obj_type[1])
    #     total = obj.objects.filter(user=request.user, type=obj_type[0], date__gte=start_date,
    #         date__lte=end_date).aggregate(total=Sum('value'))['total']
    #     total = 0 if total is None else total

    #     data.append(total)

    return JsonResponse({'labels': labels, 'data': data, 'context_label': context_label})




def get_progress_data(request):
    # chosen_year = request.GET.get('chosen_year')
    # if get_what is None or get_what not in ['income', 'outcome']:
    #     return JsonResponse({'error': 'Please specify get_what parameter to be either "income or "outcome'})
    # if get_what == 'income':
    #     obj = Income
    #     obj_types = Income.ITypes
    # else:
    #     obj = Outcome
    #     obj_types = Outcome.OTypes

    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()
    user_saving_method = Account.objects.get(user_id=request.user.id).saving_method

    today = date.today()

    translation.activate('pl')
    actual_month = date_format(today, 'F')
    actual_year = date_format(today, 'o')


    start_month = date.today().replace(day=1)
    end_month = get_last_date_of_month(today.year, today.month)

    current_today_incomes = Income.objects\
        .filter(user=request.user, date__gte=start_month, date__lte=end_month)\
        .aggregate(total=Sum('value'))['total']
    current_today_incomes = 0 if current_today_incomes is None else current_today_incomes

    print("Pbecne wydatki")
    print(current_today_incomes)

    if user_saving_method == 'METODA 6 SŁOIKÓW':
        # sloik 1 - niezbedne wydatki
        current_today_jar1 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=1, type__lte=13)\
            .aggregate(total=Sum('value'))['total']
        current_today_jar1 = 0 if current_today_jar1 is None else current_today_jar1

        # sloik 1 - cel
        current_today_goal_jar1 = round(Decimal(0.55) * current_today_incomes, 2)

        print(current_today_goal_jar1)

        # sloik 2 - duze/niespodziewane wydatki
        current_today_jar2 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=14, type__lte=20)\
            .aggregate(total=Sum('value'))['total']
        current_today_jar2 = 0 if current_today_jar2 is None else current_today_jar2

        # sloik 3 - przyjemności i rozrywka
        current_today_jar3 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=21, type__lte=37)\
            .aggregate(total=Sum('value'))['total']
        current_today_jar3 = 0 if current_today_jar3 is None else current_today_jar3

        # sloik 4 - edukacja
        current_today_jar4 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=38, type__lte=41)\
            .aggregate(total=Sum('value'))['total']
        current_today_jar4 = 0 if current_today_jar4 is None else current_today_jar4

        # sloik 5 - oszczednosci i inwestycje
        current_today_jar5 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=42, type__lte=51)\
            .aggregate(total=Sum('value'))['total']
        current_today_jar5 = 0 if current_today_jar5 is None else current_today_jar5

        # sloik 2,3,4,5 - cel
        current_today_goal_jar2345 = round(Decimal(0.1) * current_today_incomes, 2)

        # sloik 6 - pomoc innym/dobroczynnosc
        current_today_jar6 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=52, type__lte=54)\
            .aggregate(total=Sum('value'))['total']
        current_today_jar6 = 0 if current_today_jar6 is None else current_today_jar6

        # sloik 6 - cel
        current_today_goal_jar6 = round(Decimal(0.05) * current_today_incomes, 2)
    
    elif user_saving_method == 'METODA 50/30/20':
        current_today_box50 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=1, type__lte=20)\
            .aggregate(total=Sum('value'))['total']
        current_today_box50 = 0 if current_today_box50 is None else current_today_box50

        # sloik 1 - cel
        current_today_goal_box50 = round(Decimal(0.5) * current_today_incomes, 2)

        print(current_today_goal_box50)

        # sloik 2 - duze/niespodziewane wydatki
        current_today_box30 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=21, type__lte=41)\
            .aggregate(total=Sum('value'))['total']
        current_today_box30 = 0 if current_today_box30 is None else current_today_box30

        # sloik 1 - cel
        current_today_goal_box30 = round(Decimal(0.3) * current_today_incomes, 2)

        # sloik 3 - przyjemności i rozrywka
        current_today_box20 = Outcome.objects\
            .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=42, type__lte=51)\
            .aggregate(total=Sum('value'))['total']
        current_today_box20 = 0 if current_today_box20 is None else current_today_box20

        # sloik 1 - cel
        current_today_goal_box20 = round(Decimal(0.2) * current_today_incomes, 2)

    else:
        ...


    dates = Income.objects.filter(user=request.user)\
                       .annotate(year=ExtractYear('date'))\
                       .values('year').order_by('year')

    labels = []
    year_data = []

    years = set()
    for year in dates:
        years.add(year['year'])
        print(year)

    years = sorted(years, reverse=True)

    month_days_30 = [4,6,9,11]


    invoices = Outcome.objects.all()
    months = invoices.dates("date", kind="month")
    for month in months:
        month_invs = invoices.filter(date__month=month.month, user=request.user)
        month_total = month_invs.aggregate(total=Sum("value")).get("total")
        print(f"Month: {month}, Total: {month_total}")

    for year in years:
        for i in range(1,13):
            start_month = date(int(year), i, 1)
            # tutaj trzeba sprawdzic czy rok przestepny
            if i == 2:
                end_month = date(int(year), i, 28)
            elif i in month_days_30:
                end_month = date(int(year), i, 30)

            else:
                end_month = date(int(year), i, 31)

            print(f"{start_month} - {end_month}")
            labels.append(date_format(start_month, 'F'))

            current_month_incomes = Income.objects\
                .filter(user=request.user, date__gte=start_month, date__lte=end_month)\
                .aggregate(total=Sum('value'))['total']
            current_month_incomes = 0 if current_month_incomes is None else current_month_incomes

            if user_saving_method == 'METODA 6 SŁOIKÓW':
                # sloik 1 - niezbedne wydatki
                current_jar1 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=1, type__lte=13)\
                    .aggregate(total=Sum('value'))['total']
                current_jar1 = 0 if current_jar1 is None else current_jar1

                # sloik 1 - cel
                current_goal_jar1 = round(Decimal(0.55) * current_month_incomes, 2)

                # sloik 2 - duze/niespodziewane wydatki
                current_jar2 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=14, type__lte=20)\
                    .aggregate(total=Sum('value'))['total']
                current_jar2 = 0 if current_jar2 is None else current_jar2

                # sloik 3 - przyjemności i rozrywka
                current_jar3 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=21, type__lte=37)\
                    .aggregate(total=Sum('value'))['total']
                current_jar3 = 0 if current_jar3 is None else current_jar3

                # sloik 4 - edukacja
                current_jar4 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=38, type__lte=41)\
                    .aggregate(total=Sum('value'))['total']
                current_jar4 = 0 if current_jar4 is None else current_jar4

                # sloik 5 - oszczednosci i inwestycje
                current_jar5 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=42, type__lte=51)\
                    .aggregate(total=Sum('value'))['total']
                current_jar5 = 0 if current_jar5 is None else current_jar5

                # sloik 2,3,4,5 - cel
                current_goal_jar2345 = round(Decimal(0.1) * current_month_incomes, 2)

                # sloik 6 - pomoc innym/dobroczynnosc
                current_jar6 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=52, type__lte=54)\
                    .aggregate(total=Sum('value'))['total']
                current_jar6 = 0 if current_jar6 is None else current_jar6

                # sloik 6 - cel
                current_goal_jar6 = round(Decimal(0.05) * current_month_incomes, 2)

                year_data.append({
                    'month': date_format(start_month, 'F'),
                    'year': year,
                    'jar1': current_jar1,
                    'goal_jar_1': current_goal_jar1,
                    'jar2': current_jar2,
                    'goal_jar_2345': current_goal_jar2345,
                    'jar3': current_jar3,
                    'jar4': current_jar4,
                    'jar5': current_jar5,
                    'goal_jar_6': current_goal_jar6,
                    'jar6': current_jar6
                    })
            elif user_saving_method == 'METODA 50/30/20':
                # sloik 1 - niezbedne wydatki
                current_box50 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=1, type__lte=20)\
                    .aggregate(total=Sum('value'))['total']
                current_box50 = 0 if current_box50 is None else current_box50

                # sloik 1 - cel
                current_goal_box50 = round(Decimal(0.5) * current_month_incomes, 2)

                # sloik 2 - duze/niespodziewane wydatki
                current_box30 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=21, type__lte=41)\
                    .aggregate(total=Sum('value'))['total']
                current_box30 = 0 if current_box30 is None else current_box30

                # sloik 1 - cel
                current_goal_box30 = round(Decimal(0.3) * current_month_incomes, 2)

                # sloik 3 - przyjemności i rozrywka
                current_box20 = Outcome.objects\
                    .filter(user=request.user, date__gte=start_month, date__lte=end_month, type__gte=42, type__lte=51)\
                    .aggregate(total=Sum('value'))['total']
                current_box20 = 0 if current_box20 is None else current_box20

                # sloik 1 - cel
                current_goal_box20 = round(Decimal(0.2) * current_month_incomes, 2)

                year_data.append({
                    'month': date_format(start_month, 'F'),
                    'year': year,
                    'box50': current_box50,
                    'goal_box50': current_goal_box50,
                    'box30': current_box30,
                    'goal_box30': current_goal_box30,
                    'box20': current_box20,
                    'goal_box20': current_goal_box20
                    })
            
            else:
                ...

    # print(dates)

    
    # if Income.objects.filter(user=request.user).exists() and Outcome.objects.filter(user=request.user).exists():
    # # at least one object satisfying query exists

    #     first_income_date = Income.objects.filter(user=request.user).order_by('date').first().date
    #     today = Income.objects.filter(user=request.user).order_by('date').last().date

    #     number_of_days_in_last_income_month = int(get_last_date_of_month(today.year, today.month)[-2:])
    #     # # first_income_date = 
    #     print(first_income_date)
    #     print(today)
    #     # month_diference = 12
    #     delta = relativedelta.relativedelta(today, first_income_date)
    #     months_difference = delta.months + (delta.years * 12)
    #     years_difference = delta.years
        
    #     print(years_difference) 


    # month_days_30 = [4,6,9,11]

    # labels = []
    # data = []

    # translation.activate('pl')


    # for i in range(1,12):
    #     start_date = date(today.year, i, 1)
    #     if i == 2:
    #         end_date = date(today.year, i, 28)
    #     elif i in month_days_30:
    #         end_date = date(today.year, i, 30)

    #     else:
    #         end_date = date(today.year, i, 31)

    # if summary_type == 'mon1':
    #     # last_balance = Balance.objects.filter(user=request.user, type=1).order_by('-date').first()
    #     # if not last_balance:
    #     #     return JsonResponse({'error': 'No current balance has been recorded. '
    #     #                         'Please add at least one current balance record. '})
        
    #     # start_date = 
    #     # end_date = today

    #     total_income_monthly_sum = []
    #     total_outcome_monthly_sum = []


    #     # all_activities_today = Activity.objects.filter(date=date.today(), user=request.user)

    #     # all_activities = Activity.objects.filter(user=request.user).order_by('date')

    #     # type_list = [activity_type['type'] for activity_type in Activity.objects.filter(user=request.user).values('type')]

    #     # print(type_list)

    #     # date_list = [activity_date['date'] for activity_date in Activity.objects.filter(user=request.user).values('date').order_by('date').distinct()]

    #     today = datetime.now()

    #     # labels = []

    #     month_days_30 = [4,6,9,11]

    #     if today.month in month_days_30:
    #         N = 30
    #     else:
    #         N = 31

    #     start_date = date(today.year, today.month, 1)
    #     end_date = get_last_date_of_month(today.year, today.month)

    #     print(start_date)
    #     print(end_date)
    #     print(N)


    #     # n_days_ago = today - timedelta(days=N)

    #     # labels.append(start_date)


    #     for i in range(1,N+1):
    #         print(i)
    #         labels.append(start_date)
    #         start_date += timedelta(days=1)

    #     print(today.month)

    #     #print("Daty",date_last14)

    #     activity_label = []

    #     # for activity in all_activities_today:
    #     #     activity_label.append(activity.type)

    #     for activity_date in labels:
    #         total = obj.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=activity_date)))['s']
    #         # if total is None:
    #         #     data.append(0)
    #         # else:
    #         data.append(total)


    #     # for i in range(1,12):
    #     #     start_date = date(today.year, i, 1)
    #     #     if i == 2:
    #     #         end_date = date(today.year, i, 28)
    #     #     elif i in month_days_30:
    #     #         end_date = date(today.year, i, 30)

    #     #     else:
    #     #         end_date = date(today.year, i, 31)

    #     #     total_income_monthly = Income.objects\
    #     #         .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
    #     #         .aggregate(total=Sum('value'))['total']

    #     #     total_outcome_monthly = Outcome.objects\
    #     #         .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
    #     #         .aggregate(total=Sum('value'))['total']

    #     #     total_income_monthly_sum.append(total_income_monthly)
    #     #     total_outcome_monthly_sum.append(total_outcome_monthly)

    #     #     daty.append(start_date)
    #     #     daty.append(end_date)

    #     #     print(daty)
    #     #     print(total_income_monthly_sum)
    #     #     print(total_outcome_monthly_sum)
            
        
    #     #     start_date = date.today().replace(day=1)
    #     #     end_date = get_last_date_of_month(today.year, today.month)
    #     #     print("Miesiace")
    #     #     print(start_date)
    #     #     print(end_date)
    #     #     print("Koniec")
        

    # elif summary_type == 'week':
    #     # start_date = date.today() - timedelta(days=7)

    #     # end_date = date.today()
    #     # print("Miesiace")
    #     # print(start_date)
    #     # print(end_date)
    #     # print("Koniec")

    #     today = datetime.now()

    #     # labels = []

    #     month_days_30 = [4,6,9,11]

    #     # if today.month in month_days_30:
    #     #     N = 30
    #     # else:
    #     #     N = 31

    #     start_date = date.today() - timedelta(days=7)

    #     end_date = date.today()
    #     N = 8

    #     # start_date = date(today.year, today.month, 1)
    #     # end_date = get_last_date_of_month(today.year, today.month)

    #     print(start_date)
    #     print(end_date)
    #     print(N)

    #     dates = []


    #     # n_days_ago = today - timedelta(days=N)

    #     # labels.append(start_date)


    #     for i in range(1,N+1):
    #         print(i)
    #         dates.append(start_date)
    #         labels.append(f"{date_format(start_date, 'D')} ({start_date})")
    #         start_date += timedelta(days=1)

    #     print(today.month)

    #     #print("Daty",date_last14)

    #     activity_label = []

    #     # for activity in all_activities_today:
    #     #     activity_label.append(activity.type)

    #     for activity_date in dates:
    #         total = obj.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=activity_date)))['s']
    #         # if total is None:
    #         #     data.append(0)
    #         # else:
    #         data.append(total)

        

    # elif summary_type == 'mon3':

    #     first_month_start_date = (date.today().replace(day=1) - timedelta(days=60)).replace(day=1)
    #     first_month_end_date = get_last_date_of_month(today.year, first_month_start_date.month)

    #     second_month_start_date = (first_month_start_date + timedelta(days=40)).replace(day=1)
    #     second_month_end_date = get_last_date_of_month(today.year, second_month_start_date.month)

    #     third_month_start_date = date.today().replace(day=1)
    #     third_month_end_date = get_last_date_of_month(today.year, today.month)

    #     start_dates = [first_month_start_date, second_month_start_date, third_month_start_date]
    #     end_dates = [first_month_end_date, second_month_end_date, third_month_end_date]

    #     for start_date,end_date in zip(start_dates, end_dates):
    #         print(f"{start_date} - {end_date}")
    #         labels.append(date_format(start_date, 'F'))
    #         total = obj.objects.filter(user=request.user, date__gte=start_date,
    #             date__lte=end_date).aggregate(total=Sum('value'))['total']
    #         data.append(total)

    #     # first_month = date_format(first_month_start_date, 'F')
    #     # second_month = date_format(second_month_start_date, 'F')
    #     # third_month = date_format(third_month_start_date, 'F')

    #     # labels1 = [first_month, second_month, third_month]


    #     # print(first_month)
    #     # print(second_month)
    #     # print(third_month)
    #     # print(labels1)




    #     # n_days_ago = today - timedelta(days=N)

    #     # labels.append(start_date)


    #     # for i in range(1,10+1):
    #     #     print(i)
    #     #     labels.append(first_month_start_date)
    #     #     first_month_start_date += timedelta(days=1)

    #     # print(today.month)

    #     #print("Daty",date_last14)


    #     # for activity in all_activities_today:
    #     #     activity_label.append(activity.type)

    #     # for activity_date in labels:
    #     #     total = obj.objects.filter(user=request.user).aggregate(s=Sum('value', filter=Q(date=activity_date)))['s']
    #     #     # if total is None:
    #     #     #     data.append(0)
    #     #     # else:
    #     #     data.append(total)

    #     # month_days_30 = [4,6,9,11]


    # elif summary_type == 'mon6':
    #     first_month_start_date = (date.today().replace(day=1) - timedelta(days=140)).replace(day=1)
    #     first_month_end_date = get_last_date_of_month(today.year, first_month_start_date.month)
        
    #     second_month_start_date = (first_month_start_date + timedelta(days=40)).replace(day=1)
    #     second_month_end_date = get_last_date_of_month(today.year, second_month_start_date.month)

    #     third_month_start_date = (second_month_start_date + timedelta(days=40)).replace(day=1)
    #     third_month_end_date = get_last_date_of_month(today.year, third_month_start_date.month)

    #     fourth_month_start_date = (third_month_start_date + timedelta(days=40)).replace(day=1)
    #     fourth_month_end_date = get_last_date_of_month(today.year, fourth_month_start_date.month)

    #     fifth_month_start_date = (fourth_month_start_date + timedelta(days=40)).replace(day=1)
    #     fifth_month_end_date = get_last_date_of_month(today.year, fifth_month_start_date.month)

    #     sixth_month_start_date = date.today().replace(day=1)
    #     sixth_month_end_date = get_last_date_of_month(today.year, today.month)

    #     start_dates = [first_month_start_date, second_month_start_date, third_month_start_date, fourth_month_start_date, fifth_month_start_date, sixth_month_start_date]
    #     end_dates = [first_month_end_date, second_month_end_date, third_month_end_date, fourth_month_end_date, fifth_month_end_date, sixth_month_end_date]

    #     for start_date,end_date in zip(start_dates, end_dates):
    #         print(f"{start_date} - {end_date}")
    #         labels.append(date_format(start_date, 'F'))
    #         total = obj.objects.filter(user=request.user, date__gte=start_date,
    #             date__lte=end_date).aggregate(total=Sum('value'))['total']
    #         data.append(total)

    
    # elif summary_type == 'year1':

    #     for i in range(1,13):
    #         start_date = date(today.year, i, 1)
    #         # tutaj trzeba sprawdzic czy rok przestepny
    #         if i == 2:
    #             end_date = date(today.year, i, 28)
    #         elif i in month_days_30:
    #             end_date = date(today.year, i, 30)

    #         else:
    #             end_date = date(today.year, i, 31)

    #         print(f"{start_date} - {end_date}")
    #         labels.append(date_format(start_date, 'F'))
    #         total = obj.objects.filter(user=request.user, date__gte=start_date,
    #             date__lte=end_date).aggregate(total=Sum('value'))['total']
    #         data.append(total)

    #         # print(start_date)
    #         # print(end_date)

    #         # total_income_monthly = Income.objects\
    #         #     .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
    #         #     .aggregate(total=Sum('value'))['total']

    #         # total_outcome_monthly = Outcome.objects\
    #         #     .filter(user=request.user, date__gte=start_date, date__lte=end_date)\
    #         #     .aggregate(total=Sum('value'))['total']

    #         # total_income_monthly_sum.append(total_income_monthly)
    #         # total_outcome_monthly_sum.append(total_outcome_monthly)

    #         # daty.append(start_date)
    #         # daty.append(end_date)

    #         # print(daty)
    #         # print(total_income_monthly_sum)
    #         # print(total_outcome_monthly_sum)
            
        
    #         # start_date = date.today().replace(day=1)
    #         # end_date = get_last_date_of_month(today.year, today.month)
    #         # print("Miesiace")
    #         # print(start_date)
    #         # print(end_date)
    #         # print("Koniec")
    
    # # elif summary_type == 'all':
    # #     last_object = obj.objects.filter(user=request.user).order_by('-date').first()
    # #     first_object = obj.objects.filter(user=request.user).order_by('-date').last()
    # #     start_date = first_object.date

    # #     end_date = last_object.date
    # #     print("Miesiace")
    # #     print(start_date)
    # #     print(end_date)
    # #     print("Koniec")

    # else:
    #     return JsonResponse({'error': 'Please specify summary_type parameter to be either current_period or year_overview'})
    
    # # labels = []
    # data = []
    # for obj_type in obj_types.choices:
    #     labels.append(obj_type[1])
    #     total = obj.objects.filter(user=request.user, type=obj_type[0], date__gte=start_date,
    #         date__lte=end_date).aggregate(total=Sum('value'))['total']
    #     total = 0 if total is None else total

    #     data.append(total)

    # print("osotatecznie")
    # print(current_goal_jar1)

    if user_saving_method == 'METODA 6 SŁOIKÓW':
        return JsonResponse({
            'current_today_jar1': current_today_jar1,
            'current_today_goal_jar1': current_today_goal_jar1,
            'current_today_jar2': current_today_jar2,
            'current_today_jar3': current_today_jar3,
            'current_today_jar4': current_today_jar4,
            'current_today_jar5': current_today_jar5,
            'current_today_goal_jar2345': current_today_goal_jar2345,
            'current_today_jar6': current_today_jar6,
            'current_today_goal_jar6': current_today_goal_jar6,
            'actual_month': actual_month,
            'actual_year': actual_year,
            'user_currency': user_currency,
            'years': list(years),
            'year_data': year_data,
        })

    elif user_saving_method == 'METODA 50/30/20':
        return JsonResponse({
            'current_today_box50': current_today_box50,
            'current_today_goal_box50': current_today_goal_box50,
            'current_today_box30': current_today_box30,
            'current_today_goal_box30': current_today_goal_box30,
            'current_today_box20': current_today_box20,
            'current_today_goal_box20': current_today_goal_box20,
            'actual_month': actual_month,
            'actual_year': actual_year,
            'user_currency': user_currency,
            'years': list(years),
            'year_data': year_data,
        })

    else:
        ...


# Generate PDF raport
def generate_PDF(request):
    get_what = request.GET.get('get_what')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    today = date.today()
    if get_what is None or get_what not in ['incomes', 'outcomes', 'balances']:
        return JsonResponse({'error': 'Please specify get_what parameter to be either "income or "outcome'})
    if get_what == 'incomes':
        obj = Income
        raport_of_what = 'przychodów'
    elif get_what == 'outcomes':
        obj = Outcome
        raport_of_what = 'wydatków'
    else:
        obj = Balance
        raport_of_what = 'kont'

    print(start_date)
    print(end_date)

    

    if get_what != 'balances':
        if start_date == '' or end_date == '':
            start_date = today.replace(day=1)
            end_date = get_last_date_of_month(today.year, today.month)
            start_date_label = start_date.strftime("%d-%m-%Y")
            end_date_label = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_label = end_date_label.strftime("%d-%m-%Y")

        else:
            start_date_label = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_label = datetime.strptime(end_date, '%Y-%m-%d')
            start_date_label = start_date_label.strftime("%d-%m-%Y")
            end_date_label = end_date_label.strftime("%d-%m-%Y")


    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()

    

    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create text object
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Verdana', 14)



    # Add some lines of text
    lines = []

    if get_what == 'balances':
        objects = obj.objects.filter(user=request.user)

        for current_object in objects:
            lines.append((f'{str(current_object.name)}    {current_object.date}    {str(current_object.value)} {user_currency}    {current_object.get_type_display()}'))
            lines.append(" ")

        textob.textLine(f'Wykaz {raport_of_what}')
        
    
    else:
        objects = obj.objects.filter(user=request.user, date__gte=start_date, date__lte=end_date)

        for current_object in objects:
            # lines.append(str(current_object.date))
            # if current_object.comment != '':
            #     lines.append(str(f'{current_object.date}        Brak komentarza        {current_object.get_type_display()}                {current_object.value} {user_currency}'))

            # else:
            lines.append((f'{str(current_object.date)}    {current_object.balance.name}    {current_object.get_type_display()}    {str(current_object.value)} {user_currency}    {current_object.comment}'))
            # lines.append(str(current_object.get_type_display()))
            lines.append(" ")
        
        textob.textLine(f'Wykaz {raport_of_what} {start_date_label} - {end_date_label}')


    print(lines)


    textob.textLine(" ")
    textob.textLine(" ")

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename=f'Raport_PDF{today}.pdf')


# Generate CSV raport
def generate_CSV(request):
    get_what = request.GET.get('get_what')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    today = date.today()
    if get_what is None or get_what not in ['incomes', 'outcomes', 'balances']:
        return JsonResponse({'error': 'Please specify get_what parameter to be either "income or "outcome'})
    if get_what == 'incomes':
        obj = Income
        raport_of_what = 'przychodów'
    elif get_what == 'outcomes':
        obj = Outcome
        raport_of_what = 'wydatków'
    else:
        obj = Balance
        raport_of_what = 'kont'

    print(start_date)
    print(end_date)

    # locale.setlocale(locale.LC_ALL, '')
    # DELIMITER = ';' if locale.localeconv()['decimal_point'] == ',' else ','

    

    if start_date == '' or end_date == '':
        start_date = today.replace(day=1)
        end_date = get_last_date_of_month(today.year, today.month)

    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=Raport_CSV{today}.csv'

    # Create a CSV writer
    # trzeba sprawdzic w polsce
    # writer = csv.writer(response, delimiter=DELIMITER)
    writer = csv.writer(response)

    if get_what == 'balances':
        objects = obj.objects.filter(user=request.user)

         # Add column headings to the csv file
        writer.writerow(['Nazwa', 'Data utworzenia', 'Kwota', 'Typ konta', 'Komentarz'])


        for current_object in objects:
            writer.writerow([current_object.name, current_object.date, current_object.value, current_object.get_type_display(), current_object.comment])
        
    else:
        objects = obj.objects.filter(user=request.user, date__gte=start_date, date__lte=end_date)

        # Add column headings to the csv file
        writer.writerow(['Data', 'Konto', 'Kategoria', 'Kwota', 'Komentarz'])


        for current_object in objects:
            writer.writerow([current_object.date, current_object.balance.name, current_object.get_type_display(), current_object.value, current_object.comment])
        
    return response


@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, 'finances/dashboard.html')

def savings(request):
    return render(request, 'finances/savings.html')

@login_required(login_url='accounts:login')
def progress(request):
    return render(request, 'finances/progress.html')

@login_required(login_url='accounts:login')
def raport_form(request):
    raport_object = request.GET.get('raport_object')
    context = {'raport_object': raport_object}
    return render(request, 'finances/raport_form.html', context)

def slchart(request):
    return render(request, 'finances/sleep_chart.html')

@login_required(login_url='accounts:login')
def stats(request):
    return render(request, 'finances/stats.html')

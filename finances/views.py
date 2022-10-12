import calendar
import json
import io
import csv
import locale
from decimal import Decimal
from dateutil import relativedelta
from datetime import date, timedelta, datetime
from django.utils.formats import date_format
from django.utils import translation
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont   
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import BalanceForm, OutcomeForm, IncomeForm
from .models import Balance, Outcome, Income
from accounts.models import Account

# Balance Views

# Balance List View
class BalanceListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Balance
    paginate_by = 10
    template_name = 'finances/objects_table.html'

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

# Balance Create View
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
                        "objectListChanged": None
                    })
                })

# Balance Update View
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
                        "objectListChanged": None
                    })
                })

@login_required(login_url='accounts:login')
def balance_list(request):
    return render(request, 'finances/balances.html')

@login_required(login_url='accounts:login')
def delete_balance(request, part_id=None):
    balance = Balance.objects.filter(id=part_id)
    if request.method == "POST":
        balance.delete()
        return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "objectListChanged": None,
                        })
                    })
    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model':'konto', 'model_name':balance[0].name})

# Outcome Views

# Outcome List View
class OutcomeListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Outcome
    paginate_by = 10
    template_name = 'finances/objects_table.html'

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

# Outcome Create View
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
                        "objectListChanged": None
                    })
                })

# Outcome Update View
class OutcomeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Outcome
    form_class = OutcomeForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Edytuj wydatek'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        old_outcome_value = Outcome.objects.filter(id=self.object.id).aggregate(total=Sum('value'))['total']
        old_outcome_balance = Outcome.objects.filter(id=self.object.id).values('balance_id')[0]['balance_id']
        self.object.save()
        balance = Balance.objects.filter(id=self.object.balance.id)
        balance_value = balance.aggregate(total=Sum('value'))['total']
        value_to_substract = self.object.value - old_outcome_value

        if old_outcome_balance != self.object.balance.id:
            old_balance = Balance.objects.filter(id = old_outcome_balance)
            old_balance_value = old_balance.aggregate(total=Sum('value'))['total']
            old_balance_value += old_outcome_value
            old_balance.update(value = old_balance_value)
            value_to_substract = self.object.value

        balance_value -= value_to_substract
        balance.update(value = balance_value)
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "objectListChanged": None
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
                            "objectListChanged": None,
                        })
                    })
    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model': 'wydatek','model_name':outcome[0].get_type_display, 'model_value':outcome[0].value, 'model_date': outcome[0].date})

def outcome_list(request):
    return render(request, 'finances/incomes_outcomes.html', context={'list_what': 'Wydatki'})

# Income Views
class IncomeListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Income
    paginate_by = 10
    template_name = 'finances/objects_table.html'

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
                        "objectListChanged": None,
                    })
                })

class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    model = Income
    form_class = IncomeForm
    template_name = 'finances/balance_income_outcome_form.html'
    extra_context = {'header': 'Edytuj przychód'}
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        old_income_value = Income.objects.filter(id=self.object.id).aggregate(total=Sum('value'))['total']
        old_income_balance = Income.objects.filter(id=self.object.id).values('balance_id')[0]['balance_id']
        self.object.save()
        balance = Balance.objects.filter(id=self.object.balance.id)
        balance_value = balance.aggregate(total=Sum('value'))['total']
        value_to_substract = self.object.value - old_income_value

        if old_income_balance != self.object.balance.id:
            old_balance = Balance.objects.filter(id = old_income_balance)
            old_balance_value = old_balance.aggregate(total=Sum('value'))['total']
            old_balance_value -= old_income_value
            old_balance.update(value = old_balance_value)
            value_to_substract = self.object.value

        balance_value += value_to_substract
        balance.update(value = balance_value)
        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "objectListChanged": None,
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
                            "objectListChanged": None,
                        })
                    })
    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model': 'przychód','model_name':income[0].get_type_display, 'model_value':income[0].value, 'model_date': income[0].date})

@login_required(login_url='accounts:login')
def income_list(request):
    return render(request, 'finances/incomes_outcomes.html', context={'list_what': 'Przychody'})

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
    start_month = date.today().replace(day=1)
    end_month = get_last_date_of_month(today.year, today.month)
    
    # last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    # prev_start_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

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
    # average_incomes_per_day = round(total_income/number_of_days_in_actual_month, 2)
    # average_outcomes_per_day = round(total_outcome/number_of_days_in_actual_month, 2)

    # Savings
    # total_saving_balance = Balance.objects\
    #     .filter(user=request.user, type=2).aggregate(total=Sum('value'))['total']
    # total_saving_balance = 0 if total_saving_balance is None else total_saving_balance
    # last_total_balance = Balance.objects\
    #     .filter(user=request.user, type=2, date__gte=prev_start_month, date__lte=last_day_of_prev_month).aggregate(total=Sum('value'))['total']
    # last_total_balance = 0 if last_total_balance is None else last_total_balance
    # savings = total_saving_balance - last_total_balance

    # Last 5 outcomes
    last_five_outcomes_model = Outcome.objects.filter(user=request.user)[:5]
    last_five_outcomes = []
    for outcome in last_five_outcomes_model:
        last_five_outcomes.append({'id': outcome.id, 'type': outcome.get_type_display(), 'date': outcome.date.strftime("%d-%m-%Y"), 'value': str(outcome.value).replace('.', ',')})

    # Last 5 incomes
    last_five_incomes_model = Income.objects.filter(user=request.user)[:5]
    last_five_incomes = []
    for income in last_five_incomes_model:
        last_five_incomes.append({'id': income.id, 'type': income.get_type_display(), 'date': income.date.strftime("%d-%m-%Y"), 'value': str(income.value).replace('.', ',')})


    translation.activate('pl')
    actual_month = date_format(today, 'F')

    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()

    return JsonResponse({
        'total_balance': str(total_balance).replace('.', ','),
        'total_savings': str(total_savings).replace('.', ','),
        'total_income': str(total_income).replace('.', ','),
        'total_outcome': str(total_outcome).replace('.', ','),
        'today_total_income': str(today_total_income).replace('.', ','),
        'today_total_outcome': str(today_total_outcome).replace('.', ','),
        'actual_month': actual_month,
        # 'savings': savings,
        'last_five_outcomes': last_five_outcomes,
        'last_five_incomes': last_five_incomes,
        # 'average_incomes_per_day': str(average_incomes_per_day).replace('.', ','),
        # 'average_outcomes_per_day': str(average_outcomes_per_day).replace('.', ','),
        'user_currency': user_currency,
    })

def get_statistics_data(request):
    today = date.today()
    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()

    first_income_date = Income.objects.filter(user=request.user).order_by('date').first().date if Income.objects.filter(user=request.user).exists() else today
    first_outcome_date = Outcome.objects.filter(user=request.user).order_by('date').first().date if Outcome.objects.filter(user=request.user).exists() else today
    first_income_outcome_date = min(first_income_date, first_outcome_date)
    print(f"pierwsza daata to: {first_income_outcome_date}")

    monday1 = (first_income_outcome_date - timedelta(days=first_income_outcome_date.weekday()))
    monday2 = (today - timedelta(days=today.weekday()))
    days_difference = (today - first_income_outcome_date).days
    weeks_difference = Decimal((monday2 - monday1).days / 7)
    months_difference = Decimal(days_difference / 30)
    if months_difference < 1:
        months_difference = 0
    years_difference = Decimal(days_difference / 365)
    if years_difference < 1:
        years_difference = 0

   
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



def get_incomes_vs_outcomes_chart(request):
    context_label = Account.objects.get(user_id=request.user.id).get_currency_display()
    today = datetime.now()    
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
        # tutaj czy rok przystępny trzeba sprawdzić co do lutego
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

    return JsonResponse({
        'month_labels': month_labels,
        'total_income_monthly_sum': total_income_monthly_sum,
        'total_outcome_monthly_sum': total_outcome_monthly_sum,
        'context_label': context_label
    })


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

    # print(start_date)
    # print(end_date)

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

    # print(lines)

    textob.textLine(" ")
    textob.textLine(" ")

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

    locale.setlocale(locale.LC_ALL, '')
    DELIMITER = ';' if locale.localeconv()['decimal_point'] == ',' else ','


    if start_date == '' or end_date == '':
        start_date = today.replace(day=1)
        end_date = get_last_date_of_month(today.year, today.month)

    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=Raport_CSV{today}.csv'

    # Create a CSV writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=DELIMITER)
    # writer = csv.writer(response)

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

@login_required(login_url='accounts:login')
def stats(request):
    return render(request, 'finances/stats.html')

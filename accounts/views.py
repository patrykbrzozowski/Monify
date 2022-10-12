import json
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from finances.models import Balance, Income, Outcome
from .forms import CustomUserCreationForm, CustomUserChangeForm, ChangeUserCurrency, ChangeUserSavingMethod
from .models import Account

# registration function
def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            user = User.objects.get(username=email)
            Balance.objects.create(value=0, date=datetime.today(), type=1, name="Karta", user=user)
            Balance.objects.create(value=0, date=datetime.today(), type=1, name="Gotówka", user=user)
            Account.objects.create(user=user, currency='PLN', saving_method='METODA 6 SŁOIKÓW', user_id=user.id)
            messages.success(request, f'Pomyślnie zarejestrowano użytkownika o adresie email: {email}.')
    context = {'form': form}

    return render(request, 'accounts/register.html', context)

# login function
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, mark_safe(f'Jesteś już zalogowany/a jako <b>{request.user.username}</b>.'))
        return redirect('finances:dashboard')
    username = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('finances:dashboard')
        else:
            messages.warning(request, 'Podany login lub hasło są nieprawidłowe.')

    return render(request, 'accounts/login.html', context={'username': username})

# logout function
def logout_view(request):
    logout(request)
    messages.success(request, 'Wylogowano pomyślnie.')

    return redirect('accounts:login')

# This function allows user to change default currency
@login_required(login_url='accounts:login')
def change_currency(request):
    current_user_account = Account.objects.get(user_id=request.user.id)
    form = ChangeUserCurrency(request.POST or None, instance=current_user_account)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "profileDataChanged": None,
                        })
                    })
    context = {'form': form, 'header': 'currency'}

    return render(request, 'accounts/accounts_details_form.html', context)

# This function allows user to change default saving method
@login_required(login_url='accounts:login')
def change_saving_method(request):
    current_user_account = Account.objects.get(user_id=request.user.id)
    form = ChangeUserSavingMethod(request.POST or None, instance=current_user_account)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "profileDataChanged": None,
                        })
                    })
    context = {'form': form, 'header': 'saving_method'}

    return render(request, 'accounts/accounts_details_form.html', context)

# This function allows user to change profile data such as name, surname, etc.
@login_required(login_url='accounts:login')
def edit_profile(request):
    current_user = User.objects.get(id=request.user.id)
    user = request.user
    form = CustomUserChangeForm(user, request.POST or None, instance=current_user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "profileDataChanged": None,
                        })
                    })
    context = {'form': form, 'header': 'edit_profile'}

    return render(request, 'accounts/edit_profile.html', context)

# This function allows user to clear all data (all balances, all icomes and all outcomes) at once
def delete_all_data(request):
    balances = Balance.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    outcomes = Outcome.objects.filter(user=request.user)
    if request.method == "POST":
        balances.delete()
        incomes.delete()
        outcomes.delete()
        return HttpResponse(status=204)

    return render(request, 'finances/balance_income_outcome_confirm_delete.html', context={'model':'all_data'})

@login_required(login_url='accounts:login')
def get_profile_data(request):
    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()
    user_saving_method = Account.objects.get(user_id=request.user.id).get_saving_method_display()
    
    return render(request, 'accounts/get_profile_data.html', context={'user_currency': user_currency,'user_saving_method':user_saving_method})

@login_required(login_url='accounts:login')
def profile(request):
    return render(request, 'accounts/profile.html')

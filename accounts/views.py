from datetime import datetime
import json
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserChangeForm, ChangeUserCurrency, ChangeUserSavingMethod
from .models import Account
from finances.models import Balance, Income, Outcome


def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # otp = randint(1000,9999)
            # request.session['email_otp'] = otp
            # message = f'your otp is {otp}'
            # user_email = form.cleaned_data['email']
            # request.session['user_email'] = user_email

            # send_mail(
            #     'Email verification OTP', message, settings.EMAIL_HOST_USER,[user_email],fail_silently=False
            # )
            # context = {'email': user_email}
            email = form.cleaned_data['email']
            user = User.objects.get(username=email)
            Balance.objects.create(value=0, date=datetime.today(), type=1, name="Karta", user=user)
            Balance.objects.create(value=0, date=datetime.today(), type=1, name="Gotówka", user=user)
            Account.objects.create(user=user, currency='PLN', saving_method='METODA 6 SŁOIKÓW', user_id=user.id)
            messages.success(request, f'Pomyślnie zarejestrowano użytkownika o adresie email: {email}.')
            # return redirect('accounts:email-verify')
        

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

# def create_balances(instance, registered):
#     if registered:


# def email_verification(request):
#     if request.method == "POST":
#         u_otp = request.POST['otp']
#         otp = request.session['email_otp']
#         user_email = request.session['user_email']
#         print(user_email)
#         if int(u_otp)==otp:
#             p = User.objects.filter(username=user_email)
#             p.is_active = True
#             messages.success(request, f'your email is verified now')
#             return redirect('/')
#         else:
#             messages.error(request, 'Wrong otp')
#     return render(request, 'accounts/email-verified.html')

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
            # messages.success(request, f'Zalogowano pomyślnie!')
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('finances:dashboard')

        else:
            messages.warning(request, 'Podany login lub hasło są nieprawidłowe.')

    return render(request, 'accounts/login.html', context={'username': username})

def logout_view(request):
    logout(request)
    messages.success(request, 'Wylogowano pomyślnie.')
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def change_currency(request):
    # form = ChangeUserCurrency()
    # account = Account(user=request.user)
    xd = Account.objects.get(user_id=request.user.id)
    # print("Pocz")
    # print(xd.currency)
    # print("KOinec")

    # account = Account.objects.get(pk=account_low)
    form = ChangeUserCurrency(request.POST or None, instance=xd)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # return redirect('accounts:profile_info')
            # otp = randint(1000,9999)
            # request.session['email_otp'] = otp
            # message = f'your otp is {otp}'
            # user_email = form.cleaned_data['email']
            # request.session['user_email'] = user_email

            # send_mail(
            #     'Email verification OTP', message, settings.EMAIL_HOST_USER,[user_email],fail_silently=False
            # )
            # context = {'email': user_email}
            # new_currency = form.cleaned_data['currency']
            # user = request.user
            # account = Account(user=request.user)
            # account.currency = new_currency
            # xd.update(currency=new_currency)
            # account.save()
            # print(new_currency)
            # return HttpResponseRedirect('accounts:profile_info')

            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "profileDataChanged": None,
                        })
                    })


            # Balance.objects.create(value=0, date=datetime.today(), type=1, name="Gotówka", user=user)
            # messages.success(request, f'Pomyślnie zarejestrowano użytkownika o adresie email: {email}')
            # return redirect('accounts:email-verify')
        

    context = {'form': form, 'header': 'currency'}
    return render(request, 'accounts/accounts_details_form.html', context)

@login_required(login_url='accounts:login')
def edit_profile(request):

    xd = User.objects.get(id=request.user.id)
    user = request.user


    form = CustomUserChangeForm(user, request.POST or None, instance=xd)

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
def change_saving_method(request):
    # form = ChangeUserCurrency()
    # account = Account(user=request.user)
    xd = Account.objects.get(user_id=request.user.id)
    print("Pocz")
    print(xd.currency)
    print("KOinec")

    # account = Account.objects.get(pk=account_low)
    form = ChangeUserSavingMethod(request.POST or None, instance=xd)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # return redirect('accounts:profile_info')
            # otp = randint(1000,9999)
            # request.session['email_otp'] = otp
            # message = f'your otp is {otp}'
            # user_email = form.cleaned_data['email']
            # request.session['user_email'] = user_email

            # send_mail(
            #     'Email verification OTP', message, settings.EMAIL_HOST_USER,[user_email],fail_silently=False
            # )
            # context = {'email': user_email}
            # new_currency = form.cleaned_data['currency']
            # user = request.user
            # account = Account(user=request.user)
            # account.currency = new_currency
            # xd.update(currency=new_currency)
            # account.save()
            # print(new_currency)
            # return HttpResponseRedirect('accounts:profile_info')

            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "profileDataChanged": None,
                        })
                    })


            # Balance.objects.create(value=0, date=datetime.today(), type=1, name="Gotówka", user=user)
            # messages.success(request, f'Pomyślnie zarejestrowano użytkownika o adresie email: {email}')
            # return redirect('accounts:email-verify')
        

    context = {'form': form, 'header': 'saving_method'}
    return render(request, 'accounts/accounts_details_form.html', context)


@login_required(login_url='accounts:login')
def get_profile_data(request):
    user_currency = Account.objects.get(user_id=request.user.id).get_currency_display()
    user_saving_method = Account.objects.get(user_id=request.user.id).get_saving_method_display()

    # return JsonResponse({
    #     'user_currency': user_currency,
    #     'user_saving_method': user_saving_method,
    # })
    return render(request, 'accounts/get_profile_data.html', context={'user_currency': user_currency,'user_saving_method':user_saving_method})

@login_required(login_url='accounts:login')
def profile(request):
    return render(request, 'accounts/profile.html')


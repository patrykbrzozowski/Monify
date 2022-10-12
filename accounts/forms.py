from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    # first_name = forms.Field(widget=forms.TextInput(attrs={
    #     'class': 'form-control form-control-user',
    #     'placeholder': 'First Name'
    # }))
    # last_name = forms.Field(widget=forms.TextInput(attrs={
    #     'class': 'form-control form-control-user',
    #     'placeholder': 'Last Name'
    # }))
    # email = forms.Field(widget=forms.EmailInput(attrs={
    #     'class': 'form-control form-control-user',
    #     'placeholder': 'Email'
    # }))
    # password1 = forms.Field(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control form-control-user',
    #     'placeholder': 'Password'
    # }), label='Password')
    # password2 = forms.Field(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control form-control-user',
    #     'placeholder': 'Confirm Password'
    # }), label='Confirm Password')

    def is_valid(self):
        is_valid = super().is_valid()

        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', 'Użytkownik o takim adresie email już istnieje.')
            is_valid = False

        return is_valid

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = instance.email
        if commit:
            instance.save()
        
        return instance

    # def clean_email(self):
    #     if User.objects.filter(email=self.cleaned_data['email']).exists():
    #         messages.warning(self.request, 'the given email is already registered')
    #         raise forms.ValidationError("the given email is already registered")
    #     return self.cleaned_data['email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, user, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        current_user = User.objects.filter(pk = user.id).get()
        self.current_user_email = getattr(current_user, 'email')

    def is_valid(self):
        is_valid = super().is_valid()
        if self.current_user_email != self.cleaned_data['email']:
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error('email', 'Użytkownik o takim adresie email już istnieje.')
                is_valid = False

        return is_valid

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = instance.email
        if commit:
            instance.save()
        
        return instance

class ChangeUserCurrency(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['currency']

class ChangeUserSavingMethod(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['saving_method']
    
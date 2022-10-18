from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    first_name = forms.Field(widget=forms.TextInput(attrs={
        'required': 'required'
    }))
    last_name = forms.Field(widget=forms.TextInput(attrs={
        'required': 'required'
    }))
    email = forms.Field(widget=forms.EmailInput(attrs={
        'required': 'required'
    }))
    password1 = forms.Field(widget=forms.PasswordInput(attrs={
        'required': 'required'
    }))
    password2 = forms.Field(widget=forms.PasswordInput(attrs={
        'required': 'required'
    }))

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

    def clean_password1(self):
        if not self.cleaned_data['password1']:
            raise forms.ValidationError("Enter a password.")
        return self.cleaned_data['password1']

    def clean_password2(self):
        if not self.cleaned_data['password2']:
            raise forms.ValidationError("Enter your password (again)")
        return self.cleaned_data['password2']

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if len(password1) < 8:
            self.add_error('password1', 'Hasło musi zawierać co najmniej 8 znaków.')

        if password1.isdigit():
            self.add_error('password1', 'Hasło nie może się składać z samych cyfr.')

        # check for 2 digits
        if sum(p.isdigit() for p in password1) < 1:
            self.add_error('password1', 'Hasło musi zawierać co najmniej 1 cyfrę.')

        if not any(p.isupper() for p in password1):
            self.add_error('password1', 'Hasło musi zawierać co najmniej 1 dużą literę.')

        if password1 and password2:
            if password1 != password2:
                self.add_error('password1', 'Hasła nie są identyczne.')
        return cleaned_data

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
    
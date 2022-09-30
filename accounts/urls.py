from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_currency/', views.change_currency, name='change_currency'),
    path('change_saving_method/', views.change_saving_method, name='change_saving_method'),
    path('profile/', views.profile, name='profile_info'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_all_data/', views.delete_all_data, name='delete_all_data'),

    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
        email_template_name = 'accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url = reverse_lazy('accounts:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
        success_url = reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

    path('get_profile_data/', views.get_profile_data, name='get_profile_data'),
]

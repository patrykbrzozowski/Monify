from django.urls import path, re_path

from finances import views

app_name = 'finances'

urlpatterns = [
    path('balance_list_get/', views.BalanceListView.as_view(), name='balance_list_get'),
    path('balances/', views.balance_list, name='balances'),
    path('balance_create/', views.BalanceCreateView.as_view(), name='balance_create'),
    path('balance_update/<int:pk>', views.BalanceUpdateView.as_view(), name='balance_update'),
    re_path(r'^balance_delete/(?P<part_id>[0-9]+)/$', views.delete_balance, name='balance_delete'),

    path('outcome_list_get/', views.OutcomeListView.as_view(), name='outcome_list_get'),
    path('outcomes/', views.outcome_list, name='outcomes'),
    path('outcome_create/', views.OutcomeCreateView.as_view(), name='outcome_create'),
    path('outcome_update/<int:pk>', views.OutcomeUpdateView.as_view(), name='outcome_update'),
    re_path(r'^outcome_delete/(?P<part_id>[0-9]+)/$', views.delete_outcome, name='outcome_delete'),

    path('income_list_get/', views.IncomeListView.as_view(), name='income_list_get'),
    path('incomes/', views.income_list, name='incomes'),
    path('income_create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('income_update/<int:pk>', views.IncomeUpdateView.as_view(), name='income_update'),
    re_path(r'^income_delete/(?P<part_id>[0-9]+)/$', views.delete_income, name='income_delete'),

    path('get_summary_data/', views.get_summary_data, name='get_summary_data'),
    path('get_statistics_data/', views.get_statistics_data, name='get_statistics_data'),
    path('get_progress_data/', views.get_progress_data, name='get_progress_data'),
    path('get_incomes_vs_outcomes_chart/', views.get_incomes_vs_outcomes_chart, name='get_incomes_vs_outcomes_chart'),
    path('get_income_or_outcome_by_type/', views.get_income_or_outcome_by_type, name='get_income_or_outcome_by_type'),
    path('get_income_or_outcome_bar_chart/', views.get_income_or_outcome_bar_chart, name='get_income_or_outcome_bar_chart'),

    path('raport_form', views.raport_form, name='raport_form'),
    path('generate_PDF', views.generate_PDF, name='generate_PDF'),
    path('generate_CSV', views.generate_CSV, name='generate_CSV'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('savings/', views.savings, name='savings'),
    path('progress/', views.progress, name='progress'),
    path('stats/', views.stats, name='stats'),
]

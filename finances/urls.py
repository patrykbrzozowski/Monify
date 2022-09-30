from django.urls import path, re_path

from finances import views

app_name = 'finances'

urlpatterns = [
    path('balance_list_get/', views.BalanceListView.as_view(), name='balance_list_get'),
    path('balance_list/', views.balance_list, name='balance_list'),
    path('balance_detail/<pk>', views.BalanceDetailView.as_view(), name='balance_detail'),
    path('balance_create/', views.BalanceCreateView.as_view(), name='balance_create'),
    path('balance_update/<int:pk>', views.BalanceUpdateView.as_view(), name='balance_update'),
    # path('create_valid_form/', views.create_valid_form, name='create_valid_form'),
    # path('balance_delete/<pk>', views.BalanceDeleteView.as_view(), name='balance_delete'),
    re_path(r'^balance_delete/(?P<part_id>[0-9]+)/$', views.delete_balance, name='balance_delete'),


    path('outcome_list_get/', views.OutcomeListView.as_view(), name='outcome_list_get'),
    path('outcome_list/', views.outcome_list, name='outcome_list'),
    # path('balance_detail/<pk>', views.BalanceDetailView.as_view(), name='balance_detail'),
    path('outcome_create/', views.OutcomeCreateView.as_view(), name='outcome_create'),
    path('outcome_update/<int:pk>', views.OutcomeUpdateView.as_view(), name='outcome_update'),
    # path('create_valid_form/', views.create_valid_form, name='create_valid_form'),
    # path('balance_delete/<pk>', views.BalanceDeleteView.as_view(), name='balance_delete'),
    re_path(r'^outcome_delete/(?P<part_id>[0-9]+)/$', views.delete_outcome, name='outcome_delete'),


    path('income_list_get/', views.IncomeListView.as_view(), name='income_list_get'),
    path('income_list/', views.income_list, name='income_list'),
    # path('balance_detail/<pk>', views.BalanceDetailView.as_view(), name='balance_detail'),
    path('income_create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('income_update/<int:pk>', views.IncomeUpdateView.as_view(), name='income_update'),
    # path('create_valid_form/', views.create_valid_form, name='create_valid_form'),
    # path('balance_delete/<pk>', views.BalanceDeleteView.as_view(), name='balance_delete'),
    re_path(r'^income_delete/(?P<part_id>[0-9]+)/$', views.delete_income, name='income_delete'),

    path('get_summary_data/', views.get_summary_data, name='get_summary_data'),
    path('get_statistics_data/', views.get_statistics_data, name='get_statistics_data'),
    path('get_progress_data/', views.get_progress_data, name='get_progress_data'),
    # path('get_savings_data/', views.get_savings_data, name='get_savings_data'),
    # path('get_balance_chart/', views.get_balance_chart, name='get_balance_chart'),

    # path('get_year_chart/', views.get_year_chart, name='get_year_chart'),
    path('get_year_chart_custom/', views.get_year_chart_custom, name='get_year_chart_custom'),
    path('get_income_or_outcome_by_type/', views.get_income_or_outcome_by_type, name='get_income_or_outcome_by_type'),
    path('get_income_or_outcome_bar_chart/', views.get_income_or_outcome_bar_chart, name='get_income_or_outcome_bar_chart'),
    # path('get_progressbar_data/', views.get_progressbar_data, name='get_progressbar_data'),

    path('raport_form', views.raport_form, name='raport_form'),
    path('generate_PDF', views.generate_PDF, name='generate_PDF'),
    path('generate_CSV', views.generate_CSV, name='generate_CSV'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('savings/', views.savings, name='savings'),
    path('slchart/', views.slchart, name='slchart'),
    path('progress/', views.progress, name='progress'),
    path('stats/', views.stats, name='stats'),
]

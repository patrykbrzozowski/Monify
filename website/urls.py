from django.urls import path
from . import views


app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('app_info/', views.app_info, name='app_info'),
    path('methods_info/', views.methods_info, name='methods_info'),
]
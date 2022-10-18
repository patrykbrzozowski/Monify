from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('finances/', include('finances.urls')),
    path('accounts/', include('accounts.urls')),
]

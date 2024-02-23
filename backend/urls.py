# backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('creditapp.urls')),
    path('admin/', admin.site.urls),
]

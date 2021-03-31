from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.management, name='management'),
    path('add_basketball', views.add_basketball, name='add_basketball'),
    path('add_baseball', views.add_baseball, name='add_baseball'),
]

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.management, name='management'),
    path('add_basketball', views.add_basketball, name='add_basketball'),
    path('add_baseball_away',
         views.add_baseball_away, name='add_baseball_away'),
    path('add_baseball_home',
         views.add_baseball_home, name='add_baseball_home'),
    path('add_pitcher', views.add_pitcher, name='add_pitcher'),
]

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
     path('add_pitcher_away', views.add_pitcher_away, name='add_pitcher_away'),
     path('add_pitcher_home', views.add_pitcher_home, name='add_pitcher_home'),
     path('final_scores', views.final_scores, name='final_scores'),
     path('edit_gamelines/<int:game_id>/',
          views.edit_gamelines, name='edit_gamelines'),
     path('holding', views.holding, name='holding'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('mlb_matchups', views.mlb_matchup, name='mlb_matchup'),
]

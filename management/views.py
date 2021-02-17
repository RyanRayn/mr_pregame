import requests
from django.shortcuts import render
from .forms import BasketballGame
import datetime
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.boxscore import Boxscores
from sportsipy.ncaab.schedule import Schedule
from .models import Team, League, Season, Game


def management(request):
    """ View to return site management page """
    team = 'PURDUE'
    team_schedule = Schedule(team)
    schedule = list((team_schedule))
    for game in schedule:
        date = game.date
        date_time_date = datetime.datetime.strptime(date, '%a, %b %d, %Y')
        print(date_time_date.date())

    context = {
        'team': team,
        'schedule': schedule,
    }

    return render(request, 'management/management.html',
                  context)


def add_basketball(request):
    """ Add a basketball game to database """

    form = BasketballGame()
    template = 'management/add_basketball.html'
    context = {
        'form': form
    }

    return render(request, template, context)

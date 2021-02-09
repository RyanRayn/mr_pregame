import requests
from django.shortcuts import render

from datetime import datetime
from sportsipy.ncaab.boxscore import Boxscores
from sportsipy.ncaab.schedule import Schedule


def games(request):
    """ View to return games page """

    team_schedule = Schedule('PURDUE')
    for game in team_schedule:
        print(game.boxscore.away_total_rebounds)

    context = {
        'team_schedule': team_schedule,
    }

    return render(request, 'games/games.html', context)

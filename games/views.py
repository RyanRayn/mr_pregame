from django.shortcuts import render

from datetime import datetime
from sportsipy.ncaab.schedule import Schedule
from sportsipy.ncaab.boxscore import Boxscores


def games(request):
    """ View to return index page """

    return render(request, 'games/games.html')


games_today = Boxscores(datetime.today())
print(games_today.games)

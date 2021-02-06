import requests

from django.shortcuts import render
from django.conf import settings


def games(request):
    """ View to return games page """

    games_by_date = 'https://sportsdata.io/developers/api-documentation/ncaa-basketball#/scores/games-by-date'

    params = {
        'key': settings.SPORTSDATA_KEY,
        'date': '2021-FEB-06',
    }

    context = {
        'games': games
    }

    r = requests.get(games_by_date, params=params)
    print(games)
    return render(request, 'games/games.html', context)

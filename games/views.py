import requests

from django.shortcuts import render
from django.conf import settings


def games(request):
    """ View to return games page """

    date = '2021-FEB-06'
    key = settings.SPORTSDATA_KEY
    games_by_date = 'https://api.sportsdata.io/v3/cbb/scores/json/TeamGameStatsByDate/'

    query_url = f"{games_by_date}{date}?key={key}"

    r = requests.get(query_url)

    results = r.json()

    context = {
        'results': results,
    }

    return render(request, 'games/games.html', context)

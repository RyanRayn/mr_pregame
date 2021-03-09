import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime


def games(request):
    """ View to return games page """

    url = "https://sportspage-feeds.p.rapidapi.com/games?league=NCAAB"

    headers = {
        'x-rapidapi-key': settings.SPORTSPAGE_FEEDS_KEY,
        'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com"
        }

    results = requests.request("GET", url, headers=headers).json()
    games = results['results']
    for game in games:
        date = game['schedule']['date']
        datetime_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        game['game_date'] = datetime_date.strftime('%B %d, %Y')
        game['game_time'] = datetime_date.strftime('%-I:%M %p')

    context = {
        'games': games,
    }

    return render(request, 'games/games.html', context)

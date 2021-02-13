import requests
from django.shortcuts import render


def games(request):
    """ View to return games page """

    url = "https://sportspage-feeds.p.rapidapi.com/games?league=NCAAB"

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com"
        }

    games = requests.request("GET", url, headers=headers).json()

    print(type(games))

    context = {
        'games': games
    }

    return render(request, 'games/games.html', context)

import requests
from django.shortcuts import render
from django.conf import settings
import datetime


def games(request):
    """ View to return games page """
    if request.method == "POST":
        tomorrows_games = request.POST.get('date')
       
    params = {"league": "ncaab", "date": ""}

    url = "https://sportspage-feeds.p.rapidapi.com/games"

    headers = {
        'x-rapidapi-key': settings.SPORTSPAGE_FEEDS_KEY,
        'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com"
        }

    results = requests.request("GET", url,
                               headers=headers,
                               params=params).json()

    games = results['results']
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    for game in games:
        gamedate = game['schedule']['date']
        datetime_date = datetime.datetime.strptime(
                                                   gamedate,
                                                   '%Y-%m-%dT%H:%M:%S.%fZ')
        game['game_date'] = datetime_date.strftime('%B %d, %Y')
        game['game_time'] = datetime_date.strftime('%-I:%M %p')
        if 'scoreboard' in game and 'score' in game['scoreboard']:
            score = game['scoreboard']['score']
            game['total'] = score['home'] + score['away']

    context = {
        'games': games,
        'today': today,
        'tomorrow': tomorrow,
    }

    return render(request, 'games/games.html', context)

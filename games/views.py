import requests
from django.shortcuts import render
from django.conf import settings
import datetime
from pytz import timezone


def games(request):
    """ View to return games page """
    todays_date = datetime.datetime.now(timezone('America/Los_Angeles'))
    today = todays_date.strftime('%Y-%m-%d')
    tomorrow = todays_date + datetime.timedelta(days=1)
    print(todays_date)

    if request.method == "GET":
        gameday = request.GET.get('gameDate')
        league = request.GET.get('leagueName')

    params = {"league": league, "date": gameday}

    url = "https://sportspage-feeds.p.rapidapi.com/games"

    headers = {
        'x-rapidapi-key': settings.RAPID_API_KEY,
        'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com"
    }

    results = requests.request("GET", url,
                               headers=headers,
                               params=params).json()

    games = results['results']

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
        'gameday': gameday,
        'league': league,
    }

    return render(request, 'games/games.html', context)

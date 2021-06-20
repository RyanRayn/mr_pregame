import requests
from django.conf import settings
import datetime
import pytz
from management.models import MLBGameLine


def gameline(request):
    """ View to return games page """

    # Get the date for the SportspageFeeds API params
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    today = todays_date.strftime('%Y-%m-%d')

    params = {"league": league_name, 'date': today}

    url = "https://sportspage-feeds.p.rapidapi.com/games"

    headers = {
        'x-rapidapi-key': settings.RAPID_API_KEY,
        'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com"
    }

    results = requests.request("GET", url,
                               headers=headers,
                               params=params).json()

    games = results['results']

    print(games)
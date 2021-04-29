from django.shortcuts import render
import requests
from django.conf import settings
import datetime
import pytz
import tweepy
from management.models import MLBGameLine, MLBGame, TeamName


def matchups(request):
    """ a view to show MLB game matchups """
    # Get all objects in MLBGameLine model
    game_lines = MLBGameLine.objects.all()

    # Get game id from submitted form to show specific game info
    # Get city from form for weather API
    # Get league from form to render correct Matchup template

    if request.method == "GET":
        game_id = request.GET.get('gameId')
        city = request.GET.get('city')
        league = request.GET.get('league')

    # Convert game_id from to an int to match game.game_id on matchup template

    gameID = int(game_id)

    # Get currently selected game for template
    current = MLBGameLine.objects.get(gameID=gameID)

    # OpenWeatherMap API
    country = ",us"
    cityWeather = city + country
    params = {"q": cityWeather, "units": "imperial"}

    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    headers = {
        'x-rapidapi-key': settings.RAPID_API_KEY,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

    results = requests.request("GET", url,
                               headers=headers, params=params).json()
    weather_data = results['list']

    for weather in weather_data:
        current_tz = pytz.timezone("UTC")
        new_tz = pytz.timezone("US/Eastern")
        weather_date = weather['dt_txt']
        weatherDatetime = datetime.datetime.strptime(
                                                 weather_date,
                                                 '%Y-%m-%d %H:%M:%S')
        localized_time = current_tz.localize(weatherDatetime)
        gameDayWeather = localized_time.astimezone(new_tz)
        weather['gameDate'] = gameDayWeather.strftime("%B %d, %Y")
        weather['gameTime'] = gameDayWeather.strftime("%-I%p")
        weather['gameTemp'] = round(weather['main']['temp'])
        weather['gameWeather'] = weather['weather'][0]['main']

    # Twitter/Tweepy Access Keys
    auth = tweepy.OAuthHandler(
        settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_SECRET_ACCESS_TOKEN)

    home_team = current.home_team
    home_object = TeamName.objects.get(name=home_team)
    home_twitter = home_object.twitter_id
    print(home_twitter)

    context = {
        'weather_data': weather_data,
        'game_lines': game_lines,
        'league': league,
        'current': current,
    }

    return render(request, 'matchups/matchups.html', context)

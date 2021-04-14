from django.shortcuts import render
import requests
from django.conf import settings
from pprint import pprint
import datetime
import pytz


def matchups(request):
    """ a view to show MLB game matchups """

    if request.method == "GET":
        summary = request.GET.get('summary')
        league = request.GET.get('league')
        homeTeam = request.GET.get('homeFull')
        awayTeam = request.GET.get('awayFull')
        date = request.GET.get('date')
        time = request.GET.get('time')
        venue = request.GET.get('venue')
        city = request.GET.get('city')
        state = request.GET.get('state')
        awayAbbr = request.GET.get('awayAbbr')
        homeAbbr = request.GET.get('homeAbbr')
        awaySpread = request.GET.get('awaySpread')
        homeSpread = request.GET.get('homeSpread')
        awayOdds = request.GET.get('awayOdds')
        homeOdds = request.GET.get('homeOdds')
        homeML = request.GET.get('homeML')
        awayML = request.GET.get('awayML')
        total = request.GET.get('total')
        over = request.GET.get('over')
        under = request.GET.get('under')

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
        weather_date = weather['dt_txt']
        weatherDatetime = datetime.datetime.strptime(
                                                 weather_date,
                                                 '%Y-%m-%d %H:%M:%S')
        weather['gameDate'] = weatherDatetime.strftime("%B %d, %Y")
        weather['gameTime'] = weatherDatetime.strftime("%-I%p")
        weather['gameTemp'] = round(weather['main']['temp'])
        weather['gameWeather'] = weather['weather'][0]['main']

    context = {
        'summary': summary,
        'league': league,
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
        'date': date,
        'time': time,
        'venue': venue,
        'city': city,
        'state': state,
        'awayAbbr': awayAbbr,
        'homeAbbr': homeAbbr,
        'awaySpread': awaySpread,
        'homeSpread': homeSpread,
        'awayOdds': awayOdds,
        'homeOdds': homeOdds,
        'homeML': homeML,
        'awayML': awayML,
        'total': total,
        'over': over,
        'under': under,
        'weather_data': weather_data,
    }

    return render(request, 'matchups/matchups.html', context)

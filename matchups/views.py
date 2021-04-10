from django.shortcuts import render
import requests
from django.conf import settings
from pprint import pprint
import datetime


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
    data = results['list']
    for result in data:
        des = result['dt_txt']
        weatherDate = datetime.datetime.strptime(des, '%Y-%m-%d %H:%M:%S')
        pprint(weatherDate)

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
        'results': results,
    }

    return render(request, 'matchups/matchups.html', context)

import requests
from django.shortcuts import render
from django.conf import settings
import datetime
import pytz
from management.models import MLBGameLine


def games(request):
    """ View to return games page """
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
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
        game_id = game['gameId']
        gamedate = game['schedule']['date']
        summary = game['summary']
        status = game['status']
        away_team = game['teams']['away']['team']
        away_abbr = game['teams']['away']['abbreviation']
        home_team = game['teams']['home']['team']
        home_abbr = game['teams']['home']['abbreviation']
        venue = game['venue']['name']
        city = game['venue']['city']
        state = game['venue']['state']

        datetime_date = datetime.datetime.strptime(
            gamedate,
            '%Y-%m-%dT%H:%M:%S.%fZ')
        game['game_date'] = datetime_date.strftime('%B %d, %Y')
        game['game_time'] = datetime_date.strftime('%-I:%M %p')

        if 'odds' in game:
            game_odds = game['odds'][0]
            away_spread = game_odds['spread']['current']['away']
            home_spread = game_odds['spread']['current']['home']
            away_odds = game_odds['spread']['current']['awayOdds']
            home_odds = game_odds['spread']['current']['homeOdds']
            away_moneyline = game_odds['moneyline']['current']['awayOdds']
            home_moneyline = game_odds['moneyline']['current']['homeOdds']
            total = game_odds['total']['current']['total']
            over_odds = game_odds['total']['current']['overOdds']
            under_odds = game_odds['total']['current']['underOdds']

            MLBGameLine.objects.update_or_create(
                game_id=game_id, defaults={
                    'game_id': game_id,
                    'gamedate': gamedate,
                    'summary': summary,
                    'status': status,
                    'away_team': away_team,
                    'away_abbr': away_abbr,
                    'home_team': home_team,
                    'home_abbr': home_abbr,
                    'venue': venue,
                    'city': city,
                    'state': state,
                    'total': total,
                    'away_spread': away_spread,
                    'home_spread': home_spread,
                    'away_odds': away_odds,
                    'home_odds': home_odds,
                    'away_moneyline': away_moneyline,
                    'over_odds': over_odds,
                    'home_moneyline': home_moneyline,
                    'under_odds': under_odds,
                    'gameday': gameday}
            )

        elif 'scoreboard' in game and 'score' in game['scoreboard']:
            home_score = game['scoreboard']['score']['home']
            away_score = game['scoreboard']['score']['away']

            MLBGameLine.objects.update_or_create(
                game_id=game_id, defaults={
                    'home_score': home_score,
                    'away_score': away_score}
            )

        else:
            MLBGameLine.objects.update_or_create(
                game_id=game_id, defaults={
                    'game_id': game_id,
                    'gamedate': gamedate,
                    'summary': summary,
                    'status': status,
                    'away_team': away_team,
                    'away_abbr': away_abbr,
                    'home_team': home_team,
                    'home_abbr': home_abbr,
                    'venue': venue,
                    'city': city,
                    'state': state,
                    'gameday': gameday}
            )

    context = {
        'games': games,
        'today': today,
        'tomorrow': tomorrow,
        'gameday': gameday,
        'league': league,
    }

    return render(request, 'games/games.html', context)

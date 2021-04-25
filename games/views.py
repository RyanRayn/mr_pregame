import requests
from django.shortcuts import render
from django.conf import settings
import datetime
import pytz
from management.models import MLBGameLine


def games(request):
    """ View to return games page """
    # Get the date for the SportspageFeeds API params
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    today = todays_date.strftime('%Y-%m-%d')
    tomorrows_date = todays_date + datetime.timedelta(days=1)
    tomorrow = tomorrows_date.strftime('%Y-%m-%d')

    # Get data for SportspageFeeds API params
    # from form in Navbar for 'leagueName'.
    # If gameday has value from 'Tomorrow' button on games.html
    # the params will pull tomorrows games else 'today'

    if request.method == "GET":
        gameday = request.GET.get('gameDate')
        league_name = request.GET.get('leagueName')

        if gameday:
            params = {"league": league_name, "date": gameday}
        else:
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

    # SportspageFeeds API data to be directly saved into
    # db when league name is clicked in Nav.

    for game in games:
        if game['details']['league'] == 'MLB':
            gameID = game['gameId']
            timestamp = game['schedule']['date']
            summary = game['summary']
            league = game['details']['league']
            status = game['status']
            away_team = game['teams']['away']['team']
            away_abbr = game['teams']['away']['abbreviation']
            home_team = game['teams']['home']['team']
            home_abbr = game['teams']['home']['abbreviation']
            venue = game['venue']['name']
            city = game['venue']['city']
            state = game['venue']['state']

            # SportspageFeeds API timestamp is UTC time.
            # This converts it to US/Eastern.

            datetime_date = datetime.datetime.strptime(
                timestamp,
                '%Y-%m-%dT%H:%M:%S.%fZ')

            current_tz = pytz.timezone("UTC")
            new_tz = pytz.timezone("US/Eastern")
            localized_time = current_tz.localize(datetime_date)
            new_timestamp = localized_time.astimezone(new_tz)
            game['timestamp'] = new_timestamp
            game['game_date'] = new_timestamp.strftime('%B %d, %Y')
            game['game_time'] = new_timestamp.strftime('%-I:%M %p')
            gamedate = new_timestamp

            # Create new game instance in MLBGamline model
            # or update with game_id as key.

            MLBGameLine.objects.update_or_create(
                gameID=gameID, defaults={
                    'gameID': gameID,
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
                    'league': league,
                    'gameday': today}
            )

            # If the game has odds already set,
            # update or create new instance of game.

            if 'odds' in game:
                game_odds = game['odds'][0]

                # If game has 'spread' in odds set,
                # update or create new instance of game.

                if 'spread' in game_odds:
                    away_spread = game_odds['spread']['current']['away']
                    home_spread = game_odds['spread']['current']['home']
                    away_odds = game_odds['spread']['current']['awayOdds']
                    home_odds = game_odds['spread']['current']['homeOdds']

                    MLBGameLine.objects.update_or_create(
                        gameID=gameID, defaults={
                            'away_spread': away_spread,
                            'home_spread': home_spread,
                            'away_odds': away_odds,
                            'home_odds': home_odds}
                    )

                # If game has 'moneyline' in odds set,
                # update or create new instance of game.

                if 'moneyline' in game_odds:
                    awayMoneyline = game_odds['moneyline']
                    away_moneyline = awayMoneyline['current']['awayOdds']
                    homeMoneyline = game_odds['moneyline']
                    home_moneyline = homeMoneyline['current']['homeOdds']

                    MLBGameLine.objects.update_or_create(
                        gameID=gameID, defaults={
                            'away_moneyline': away_moneyline,
                            'home_moneyline': home_moneyline}
                    )

                # If the game has 'total' in odds set,
                # update or create new instance of game.

                if 'total' in game_odds:
                    total = game_odds['total']['current']['total']
                    over_odds = game_odds['total']['current']['overOdds']
                    under_odds = game_odds['total']['current']['underOdds']

                    MLBGameLine.objects.update_or_create(
                        gameID=gameID, defaults={
                            'total': total,
                            'over_odds': over_odds,
                            'under_odds': under_odds}
                    )

            # If the game is in progress or final,
            # update score or create new instance of game.

            if 'scoreboard' in game and 'score' in game['scoreboard']:
                home_score = game['scoreboard']['score']['home']
                away_score = game['scoreboard']['score']['away']

                MLBGameLine.objects.update_or_create(
                    gameID=gameID, defaults={
                        'home_score': home_score,
                        'away_score': away_score}
                )

    all_games = MLBGameLine.objects.all()

    context = {
        'games': games,
        'today': today,
        'tomorrow': tomorrow,
        'gameday': gameday,
        'league': league,
        'all_games': all_games,
        'todays_date': todays_date,
    }

    return render(request, 'games/games.html', context)

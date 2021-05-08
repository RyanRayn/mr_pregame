from django.shortcuts import render
import requests
from django.conf import settings
import datetime
import pytz
import tweepy
from management.models import MLBGameLine, MLBGame, TeamName, StartingPitcher
from django.db.models import Avg, Count, Min, Sum


def matchups(request):
    """ a view to show MLB game matchups """
    # Get the date for the SportspageFeeds API params
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    yesterdays_date = todays_date + datetime.timedelta(days=-1)
    yesterday = yesterdays_date.strftime('%Y-%m-%d')

    # Date format for carousel "if statement"
    date_LA = todays_date.strftime('%B %-d, %Y')

    # Get all objects in MLBGameLine model using for game carousel
    all_games = MLBGameLine.objects.all()

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

    # Twitter/Tweepy API
    auth = tweepy.OAuthHandler(
        settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_SECRET_ACCESS_TOKEN)

    # Get current teams Twitter handles from db
    home_object = TeamName.objects.get(name=current.home_team)
    home_twitter = home_object.twitter_id
    away_object = TeamName.objects.get(name=current.away_team)
    away_twitter = away_object.twitter_id

    api = tweepy.API(auth)

    # _user gets profile information _tweets gets status timeline
    home_user = api.get_user(screen_name=home_twitter)
    home_tweets = tweepy.Cursor(
        api.user_timeline, id=home_twitter, exclude_replies=True,
        include_rts=False).items(20)
    away_user = api.get_user(screen_name=away_twitter)
    away_tweets = tweepy.Cursor(
        api.user_timeline, id=away_twitter, exclude_replies=True,
        include_rts=False).items(20)

    # HOME TEAM STATS

    # Get all objects in MLBGame model for current game home team
    home_stats = MLBGame.objects.filter(name__name=current.home_team)
    # Home team nickname
    home_stats.nickname = home_stats[0].nickname
    # Home team total home wins
    home_stats.wins_home = home_stats.aggregate(
        Sum('win_home'))['win_home__sum']
    # Home team total home loss
    home_stats.loss_home = home_stats.aggregate(
        Sum('loss_home'))['loss_home__sum']
    # Home team total wins
    home_stats.total_wins = home_stats.aggregate(
        total=Sum('win_home') + Sum('win_away'))['total']
    # Home team total loss
    home_stats.total_loss = home_stats.aggregate(
        total=Sum('loss_home') + Sum('loss_away'))['total']
    # Home team avg runs/game
    home_stats.avg_runs = home_stats.aggregate(total=Avg('runs'))['total']
    # Home team stats last ten games
    home_stats.home_ten = home_stats.order_by('-id')[:10]
    # Home team bullpen innings pitched last ten games
    # Conversion from outs to innings
    bullpen_outs = home_stats.home_ten.aggregate(
        total=Sum('bullpen_inning_thirds'))['total']
    innings, outs = divmod(bullpen_outs, 3)
    home_stats.home_bullpen_ten = str(innings)
    if outs:
        home_stats.home_bullpen_ten += '.' + str(outs)
    # Home team bullpen ERA last ten games
    bullpen_runs = home_stats.home_ten.aggregate(
        total=Sum('bullpen_runs'))['total']
    bullpen_innings = bullpen_outs / 3
    home_stats.home_bullpen_era = (bullpen_runs / bullpen_innings) * 9
    # Home Probable Starter stats from db
    probable_home = StartingPitcher.objects.filter(
        name=current.home_starter)
    # Home Starter runs first 5
    probable_home.run_five = probable_home.aggregate(
        total=Avg('runs_first_five'))['total']
    # Home Starter total HR
    probable_home.hr = probable_home.aggregate(
        total=Sum('home_runs'))['total']
    # Home Starter avg hits/game
    probable_home.hits = probable_home.aggregate(
        total=Avg('hits'))['total']
    # Home Starter avg walks/game
    probable_home.walks = probable_home.aggregate(
        total=Avg('walks'))['total']

    # AWAY TEAM STATS

    # Get all objects in MLBGame model for current game away team
    away_stats = MLBGame.objects.filter(name__name=current.away_team)
    # Away team nickname
    away_stats.nickname = away_stats[0].nickname
    # Away team total away wins
    away_stats.wins_away = away_stats.aggregate(
        Sum('win_away'))['win_away__sum']
    # Away team total away loss
    away_stats.loss_away = away_stats.aggregate(
        Sum('loss_away'))['loss_away__sum']
    # Away team total wins
    away_stats.total_wins = away_stats.aggregate(
        total=Sum('win_home') + Sum('win_away'))['total']
    # Away team total loss
    away_stats.total_loss = away_stats.aggregate(
        total=Sum('loss_home') + Sum('loss_away'))['total']
    # Away team avg runs/game
    away_stats.avg_runs = away_stats.aggregate(total=Avg('runs'))['total']
    # Away team stats last ten games
    away_stats.away_ten = away_stats.order_by('-id')[:10]
    # Away team bullpen innings pitched last ten games
    # Conversion from outs to innings
    bullpen_outs = away_stats.away_ten.aggregate(
        total=Sum('bullpen_inning_thirds'))['total']
    innings, outs = divmod(bullpen_outs, 3)
    away_stats.away_bullpen_ten = str(innings)
    if outs:
        away_stats.away_bullpen_ten += '.' + str(outs)
    # Away team bullpen ERA last ten games
    bullpen_runs = away_stats.away_ten.aggregate(
        total=Sum('bullpen_runs'))['total']
    bullpen_innings = bullpen_outs / 3
    away_stats.away_bullpen_era = (bullpen_runs / bullpen_innings) * 9
    # Away Probable Starter stats from db
    probable_away = StartingPitcher.objects.filter(
        name=current.away_starter)
    # Away Starter runs first 5
    probable_away.run_five = probable_away.aggregate(
        total=Avg('runs_first_five'))['total']
    # Away Starter total HR
    probable_away.hr = probable_away.aggregate(
        total=Sum('home_runs'))['total']
    # Away Starter avg hits/game
    probable_away.hits = probable_away.aggregate(
        total=Avg('hits'))['total']
    # Away Starter avg walks
    probable_away.walks = probable_away.aggregate(
        total=Avg('walks'))['total']

    context = {
        'weather_data': weather_data,
        'all_games': all_games,
        'date_LA': date_LA,
        'league': league,
        'current': current,
        'home_tweets': home_tweets,
        'away_tweets': away_tweets,
        'home_user': home_user,
        'away_user': away_user,
        'away_stats': away_stats,
        'home_stats': home_stats,
        'probable_home': probable_home,
        'probable_away': probable_away,
    }

    return render(request, 'matchups/matchups.html', context)

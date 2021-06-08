from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
import datetime
import pytz
import tweepy
from management.models import MLBGameLine, MLBGame, TeamName, StartingPitcher
from profiles.models import UserProfile
from django.db.models import Avg, Sum


def mlb_matchup(request):
    """ a view to show MLB game matchups """
    profile = get_object_or_404(UserProfile, user=request.user)

    # Get the date for the SportspageFeeds API params
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))

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
    # Home team games played
    home_stats.games_played = home_stats.total_wins + home_stats.total_loss
    # Home team avg runs/game
    home_stats.avg_runs = home_stats.aggregate(total=Avg('runs'))['total']
    # Home team avg runs allowed/game
    home_stats.avg_runs_allowed = home_stats.aggregate(
        total=Avg('runs_allowed'))['total']
    # Home team avg runs first 5 innings
    home_stats.avg_runs_five = home_stats.aggregate(
        total=Avg('runs_first_five'))['total']
    # Home team avg runs allowed first 5
    home_stats.avg_runs_allowed_five = home_stats.aggregate(
        total=Avg('runs_allowed_first_five'))['total']
    # Home team total hits, at bats, BA
    home_stats.total_hits = home_stats.aggregate(total=Sum('hits'))['total']
    home_stats.total_at_bats = home_stats.aggregate(
        total=Sum('at_bats'))['total']
    home_stats.ba = home_stats.total_hits / home_stats.total_at_bats
    # Home team opponent total hits, at bats, BA
    home_stats.opponent_total_hits = home_stats.aggregate(
        total=Sum('hits_allowed'))['total']
    home_stats.opponent_total_at_bats = home_stats.aggregate(
        total=Sum('opponent_at_bats'))['total']
    home_stats.opponent_ba = (
        home_stats.opponent_total_hits / home_stats.opponent_total_at_bats)
    # Home team total HR
    home_stats.total_hr = home_stats.aggregate(total=Sum('home_runs'))['total']
    # Home team opponent HR
    home_stats.opponent_hr = home_stats.aggregate(
        total=Sum('home_runs_against'))['total']
    # Home team offensive strikeouts
    home_stats.total_k = home_stats.aggregate(total=Sum('strikeouts'))['total']
    # Home team defensive strikeouts
    home_opponent = MLBGame.objects.filter(opponent=current.home_team)
    home_stats.total_def_k = home_opponent.aggregate(
        total=Sum('strikeouts'))['total']
    # Home team total errors
    home_stats.total_errors = home_stats.aggregate(
        total=Sum('errors'))['total']

    # HOME LAST TEN GAME STATS

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
    # Home team avg runs/game last ten games
    home_stats.avg_runs_ten = home_stats.home_ten.aggregate(total=Avg('runs'))['total']
    # Home team avg runs allowed/game last ten games
    home_stats.avg_runs_allowed_ten = home_stats.home_ten.aggregate(
        total=Avg('runs_allowed'))['total']
    # Home team avg runs first 5 innings last ten games
    home_stats.avg_runs_five_ten = home_stats.home_ten.aggregate(
        total=Avg('runs_first_five'))['total']
    # Home team avg runs allowed first 5 last ten games
    home_stats.avg_runs_allowed_five_ten = home_stats.home_ten.aggregate(
        total=Avg('runs_allowed_first_five'))['total']        
    # Home team total wins last ten games
    home_home_wins = home_stats.home_ten.aggregate(
        total=Sum('win_home'))['total']
    home_away_wins = home_stats.home_ten.aggregate(
        total=Sum('win_away'))['total']
    home_stats.wins_ten = home_home_wins + home_away_wins
    # Home team total loss last ten games
    home_home_loss = home_stats.home_ten.aggregate(
        total=Sum('loss_home'))['total']
    home_away_loss = home_stats.home_ten.aggregate(
        total=Sum('loss_away'))['total']
    home_stats.loss_ten = home_home_loss + home_away_loss
    # Home team total home runs last ten games
    home_stats.hr_ten = home_stats.home_ten.aggregate(
        total=Sum('home_runs'))['total']
    # Home team avg hits/game, at bats, BA last ten games
    home_stats.hits_ten = home_stats.home_ten.aggregate(
        total=Sum('hits'))['total']
    home_stats.last_ten_at_bats = home_stats.home_ten.aggregate(
        total=Sum('at_bats'))['total']
    home_stats.ba_ten = home_stats.hits_ten / home_stats.last_ten_at_bats
    # Home team opponent total hits, at bats, BA last ten games
    home_stats.opponent_hits_ten = home_stats.home_ten.aggregate(
        total=Sum('hits_allowed'))['total']
    home_stats.opponent_last_ten_at_bats = home_stats.home_ten.aggregate(
        total=Sum('opponent_at_bats'))['total']
    home_stats.opponent_ba_ten = (
        home_stats.opponent_hits_ten / home_stats.opponent_last_ten_at_bats)
    # Home team total strikeouts last ten
    home_stats.k_ten = home_stats.home_ten.aggregate(
        total=Sum('strikeouts'))['total']
    # Home team total errors last ten
    home_stats.total_errors_ten = home_stats.home_ten.aggregate(
        total=Sum('errors'))['total']


    # HOME PROBABLE STARTER

    # Home Probable Starter stats from db
    probable_home = StartingPitcher.objects.filter(
        name=current.home_starter)
    if probable_home:
        # Home Starter runs first 5
        probable_home.run_five = probable_home.aggregate(
            total=Avg('runs_first_five'))['total']
        # Home Starter total HR
        probable_home.hr = probable_home.aggregate(
            total=Sum('home_runs'))['total']
        # Home Starter avg hits per 9
        home_hits = probable_home.aggregate(total=Sum('hits'))['total']
        home_innings = probable_home.aggregate(
            total=Sum('inning_thirds'))['total'] / 3
        probable_home.hits = (home_hits / home_innings) * 9
        # Home Starter avg walks/game
        home_walks = probable_home.aggregate(
            total=Sum('walks'))['total']
        probable_home.walks = (home_walks / home_innings) * 9

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
    # Away team games played
    away_stats.games_played = away_stats.total_wins + away_stats.total_loss
    # Away team avg runs/game
    away_stats.avg_runs = away_stats.aggregate(total=Avg('runs'))['total']
    # Away team avg runs allowed/game
    away_stats.avg_runs_allowed = away_stats.aggregate(
        total=Avg('runs_allowed'))['total']
    # Away team avg runs first 5 innings
    away_stats.avg_runs_five = away_stats.aggregate(
        total=Avg('runs_first_five'))['total']
    # Away team avg runs allowed first 5
    away_stats.avg_runs_allowed_five = away_stats.aggregate(
        total=Avg('runs_allowed_first_five'))['total']
    # Away team avg hits/game, at bats, BA
    away_stats.total_hits = away_stats.aggregate(
        total=Sum('hits'))['total']
    away_stats.total_at_bats = away_stats.aggregate(
        total=Sum('at_bats'))['total']
    away_stats.ba = away_stats.total_hits / away_stats.total_at_bats
    # Away team opponent total hits, at bats, BA
    away_stats.opponent_total_hits = away_stats.aggregate(
        total=Sum('hits_allowed'))['total']
    away_stats.opponent_total_at_bats = away_stats.aggregate(
        total=Sum('opponent_at_bats'))['total']
    away_stats.opponent_ba = (
        away_stats.opponent_total_hits / away_stats.opponent_total_at_bats)
    # Away team total HR
    away_stats.total_hr = away_stats.aggregate(total=Sum('home_runs'))['total']
    # Away team opponent HR
    away_stats.opponent_hr = away_stats.aggregate(
        total=Sum('home_runs_against'))['total']
    # Away team offensive strikeouts
    away_stats.total_k = away_stats.aggregate(total=Sum('strikeouts'))['total']
    # Away team defensive strikeouts
    away_opponent = MLBGame.objects.filter(opponent=current.away_team)
    away_stats.total_def_k = away_opponent.aggregate(
        total=Sum('strikeouts'))['total']
    # Away team total errors
    away_stats.total_errors = away_stats.aggregate(
        total=Sum('errors'))['total']

    # AWAY LAST TEN GAME STATS

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
    # Away team avg runs/game last ten games
    away_stats.avg_runs_ten = away_stats.away_ten.aggregate(total=Avg('runs'))['total']
    # Away team avg runs allowed/game last ten games
    away_stats.avg_runs_allowed_ten = away_stats.away_ten.aggregate(
        total=Avg('runs_allowed'))['total']
    # Away team avg runs first 5 innings last ten games
    away_stats.avg_runs_five_ten = away_stats.away_ten.aggregate(
        total=Avg('runs_first_five'))['total']
    # Away team avg runs allowed first 5 last ten games
    away_stats.avg_runs_allowed_five_ten = away_stats.away_ten.aggregate(
        total=Avg('runs_allowed_first_five'))['total']           
    # Away team total wins last ten games
    away_home_wins = away_stats.away_ten.aggregate(
        total=Sum('win_home'))['total']
    away_away_wins = away_stats.away_ten.aggregate(
        total=Sum('win_away'))['total']
    away_stats.wins_ten = away_home_wins + away_away_wins
    # Away team total loss last ten games
    away_home_loss = away_stats.away_ten.aggregate(
        total=Sum('loss_home'))['total']
    away_away_loss = away_stats.away_ten.aggregate(
        total=Sum('loss_away'))['total']
    away_stats.loss_ten = away_home_loss + away_away_loss
    # Away team total home runs last ten games
    away_stats.hr_ten = away_stats.away_ten.aggregate(
        total=Sum('home_runs'))['total']
    # Away team avg hits/game, at bats, BA last ten games
    away_stats.hits_ten = away_stats.away_ten.aggregate(
        total=Sum('hits'))['total']
    away_stats.last_ten_at_bats = away_stats.away_ten.aggregate(
        total=Sum('at_bats'))['total']
    away_stats.ba_ten = away_stats.hits_ten / away_stats.last_ten_at_bats
    # Away team opponent total hits, at bats, BA last ten games
    away_stats.opponent_hits_ten = away_stats.away_ten.aggregate(
        total=Sum('hits_allowed'))['total']
    away_stats.opponent_last_ten_at_bats = away_stats.away_ten.aggregate(
        total=Sum('opponent_at_bats'))['total']
    away_stats.opponent_ba_ten = (
        away_stats.opponent_hits_ten / away_stats.opponent_last_ten_at_bats)
    # Away team total strikeouts last ten
    away_stats.k_ten = away_stats.away_ten.aggregate(
        total=Sum('strikeouts'))['total']
    # Away team total errors last ten
    away_stats.total_errors_ten = away_stats.away_ten.aggregate(
        total=Sum('errors'))['total']


    # AWAY PROBABLE STARTER

    # Away Probable Starter stats from db
    probable_away = StartingPitcher.objects.filter(
        name=current.away_starter)
    if probable_away:
        # Away Starter runs first 5
        probable_away.starts = probable_away.count()
        probable_away.run_five = probable_away.aggregate(
            total=Avg('runs_first_five'))['total']
        # Away Starter total HR
        probable_away.hr = probable_away.aggregate(
            total=Sum('home_runs'))['total']
        # Away Starter avg hits/game
        away_hits = probable_away.aggregate(total=Sum('hits'))['total']
        away_innings = probable_away.aggregate(
            total=Sum('inning_thirds'))['total'] / 3
        probable_away.hits = (away_hits / away_innings) * 9
        # Away Starter avg walks
        away_walks = probable_away.aggregate(
            total=Sum('walks'))['total']
        probable_away.walks = (away_walks / away_innings) * 9

    context = {
        'weather_data': weather_data,
        'all_games': all_games,
        'date_LA': date_LA,
        'league': league,
        'current': current, #MLBGameline
        'home_tweets': home_tweets, #Twitter
        'away_tweets': away_tweets, #Twitter
        'home_user': home_user, #Twitter
        'away_user': away_user, #Twitter
        'away_stats': away_stats,
        'home_stats': home_stats,
        'probable_home': probable_home,
        'probable_away': probable_away,
        'gameID': gameID,
        'profile': profile,
    }

    return render(request, 'matchups/mlb_matchup.html', context)

import requests
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AwayBaseballGames, HomeBaseballGames
from .forms import Pitcher, EditGameLine
import datetime
from sportsipy.mlb.teams import Teams as MLBTeams
from .models import MLBGame, MLBGameLine
import pytz


@login_required
def management(request):
    """ View to return site management page """

    context = {
    }

    return render(request, 'management/management.html',
                  context)


@login_required
def add_basketball(request):
    """ Add a basketball game to database """

    template = 'management/add_basketball.html'
    context = {

    }

    return render(request, template, context)


@login_required
def add_baseball_away(request):
    """ Add a baseball stats to database """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "POST":
        form = AwayBaseballGames(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added stats!')
            return redirect('/management/add_pitcher_away')
        else:
            messages.error(request,
                           "Failed to add stats.")
    else:
        form = AwayBaseballGames()

    template = 'management/add_baseball_away.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_baseball_home(request):
    """ Add a baseball stats to database """
    game = MLBGame.objects.last()

    opponent = game.name
    runs = game.runs_allowed
    runs_first_five = game.runs_allowed_first_five
    runs_allowed = game.runs
    runs_allowed_first_five = game.runs_first_five
    hits = game.hits_allowed
    hits_allowed = game.hits
    home_runs = game.home_runs_against
    home_runs_against = game.home_runs
    win_home = game.loss_away
    loss_home = game.win_away
    win_away = game.loss_home
    loss_away = game.win_home
    at_bats = game.opponent_at_bats
    opponent_at_bats = game.at_bats
    errors = game.opponent_errors

    initial = {
        'opponent': opponent,
        'runs': runs,
        'runs_first_five': runs_first_five,
        'runs_allowed': runs_allowed,
        'runs_allowed_first_five': runs_allowed_first_five,
        'hits': hits,
        'hits_allowed': hits_allowed,
        'home_runs': home_runs,
        'home_runs_against': home_runs_against,
        'win_home': win_home,
        'loss_home': loss_home,
        'win_away': win_away,
        'loss_away': loss_away,
        'at_bats': at_bats,
        'opponent_at_bats': opponent_at_bats,
        'errors': errors,
    }

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "POST":
        form = HomeBaseballGames(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added stats!')
            return redirect('/management/add_pitcher_home')
        else:
            messages.error(request,
                           "Failed to add stats.")
    else:
        form = HomeBaseballGames(initial=initial)

    template = 'management/add_baseball_home.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_pitcher_away(request):
    """ Add a baseball stats to database """
    game = MLBGame.objects.last()

    runs_first_five = game.runs_allowed_first_five

    initial = {
        'runs_first_five': runs_first_five,
    }

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "POST":
        form = Pitcher(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added stats!')
            return redirect('add_baseball_home')
        else:
            messages.error(request,
                           "Failed to add stats.")
    else:
        form = Pitcher(initial=initial)

    template = 'management/add_pitcher_away.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_pitcher_home(request):
    """ Add a baseball stats to database """
    game = MLBGame.objects.last()

    runs_first_five = game.runs_allowed_first_five

    initial = {
        'runs_first_five': runs_first_five,
    }

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "POST":
        form = Pitcher(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added stats!')
            return redirect('add_baseball_away')
        else:
            messages.error(request,
                           "Failed to add stats.")
    else:
        form = Pitcher(initial=initial)

    template = 'management/add_pitcher_home.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def final_scores(request):
    """ View to submit gamelines and info from the SportspageFeeds API """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    # Get the date for the SportspageFeeds API params
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    today = todays_date.strftime('%Y-%m-%d')
    tomorrows_date = todays_date + datetime.timedelta(days=1)
    tomorrow = tomorrows_date.strftime('%Y-%m-%d')

    # Get data from SportspageFeeds API via button click on management.html

    if request.method == "GET":

        gameday = request.GET.get('gameDate')
        league_name = request.GET.get('leagueName')

        params = {"league": league_name, "date": gameday}

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
            gameID = game['gameId']
            timestamp = game['schedule']['date']
            summary = game['summary']
            league = game['details']['league']
            away_team = game['teams']['away']['team']
            away_abbr = game['teams']['away']['abbreviation']
            home_team = game['teams']['home']['team']
            home_abbr = game['teams']['home']['abbreviation']
            venue = game['venue']['name']
            city = game['venue']['city']
            state = game['venue']['state']
            status = game['status']

            # SportspageFeeds API timestamp is UTC time.
            # This converts it to US/Eastern.

            datetime_date = datetime.datetime.strptime(
                timestamp,
                '%Y-%m-%dT%H:%M:%S.%fZ')

            current_tz = pytz.timezone("UTC")
            new_tz = pytz.timezone("US/Eastern")
            localized_time = current_tz.localize(datetime_date)
            new_timestamp = localized_time.astimezone(new_tz)
            game['game_date'] = new_timestamp.strftime('%B %d, %Y')
            game['game_time'] = new_timestamp.strftime('%-I:%M %p')
            gamedate = new_timestamp

            # Create new game instance in MLBGamline model
            # or update with game_id as key.

            MLBGameLine.objects.update_or_create(
                gameID=gameID, defaults={
                    'gameID': gameID,
                    'gamedate': gamedate,
                    'gameday': gameday,
                    'summary': summary,
                    'status': status,
                    'away_team': away_team,
                    'away_abbr': away_abbr,
                    'home_team': home_team,
                    'home_abbr': home_abbr,
                    'venue': venue,
                    'city': city,
                    'state': state,
                    'league': league}
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
                    moneyline = game_odds['moneyline']
                    away_moneyline = moneyline['current']['awayOdds']
                    home_moneyline = moneyline['current']['homeOdds']

                MLBGameLine.objects.update_or_create(
                    gameID=gameID, defaults={
                        'away_moneyline': away_moneyline,
                        'home_moneyline': home_moneyline}
                )

                # If game has 'total' in odds set,
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

    context = {
        'today': today,
        'tomorrow': tomorrow,
    }

    return render(request, context, 'management/management.html')


@login_required
def edit_gamelines(request, game_id):
    """ Edit gameline info in database """
    game = get_object_or_404(MLBGameLine, pk=game_id)

    if request.method == 'POST':
        form = EditGameLine(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated game!')
            return redirect(reverse('games'))
        else:
            messages.error(request, 'Failed to update game.')
    else:
        form = EditGameLine(instance=game)

    template = 'management/edit_gamelines.html'

    context = {
        'game': game,
        'form': form,
    }

    return render(request, template, context)

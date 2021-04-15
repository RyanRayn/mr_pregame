import requests
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AwayBaseballGames, HomeBaseballGames, Pitcher
import datetime
from sportsipy.mlb.teams import Teams as MLBTeams
from .models import BaseballGame, MLBToday
from pytz import timezone


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
    game = BaseballGame.objects.last()

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
    game = BaseballGame.objects.last()

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
    game = BaseballGame.objects.last()

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
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "GET":

        todays_date = datetime.datetime.now(timezone('America/Los_Angeles'))
        yesterday = todays_date.strftime('%Y-%m-%d')

        params = {"league": 'MLB', "date": yesterday}

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
            away_team = game['teams']['away']['team']
            away_abbr = game['teams']['away']['abbreviation']
            home_team = game['teams']['home']['team']
            home_abbr = game['teams']['home']['abbreviation']
            venue = game['venue']['name']
            city = game['venue']['city']
            state = game['venue']['state']
            status = game['status']
            if 'odds' in game:
                away_spread = game['odds'][0]['spread']['current']['away']
                home_spread = game['odds'][0]['spread']['current']['home']
                away_odds = game['odds'][0]['spread']['current']['awayOdds']
                home_odds = game['odds'][0]['spread']['current']['homeOdds']
                away_moneyline = game['odds'][0]['moneyline']['current']['awayOdds']
                home_moneyline = game['odds'][0]['moneyline']['current']['homeOdds']
                total = game['odds'][0]['total']['current']['total']
                over_odds = game['odds'][0]['total']['current']['overOdds']
                under_odds = game['odds'][0]['total']['current']['underOdds']

                MLBToday.objects.update_or_create(
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
                        'under_odds': under_odds}
                )
            else:
                MLBToday.objects.update_or_create(
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
                        'state': state}
                )
    return render(request, 'management/management.html')

import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AwayBaseballGames, HomeBaseballGames, Pitcher
from datetime import datetime
from sportsipy.nba.teams import Teams as NBATeams
from sportsipy.mlb.teams import Teams as MLBTeams
from .models import BasketballTeamStats, TeamName, Season
from .models import BaseballGame, StartingPitcher


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

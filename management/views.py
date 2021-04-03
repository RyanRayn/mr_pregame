import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BaseballGames, Pitcher
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
def add_baseball(request):
    """ Add a baseball stats to database """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "POST":
        form = BaseballGames(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added stats!')
            return redirect('/management/add_pitcher')
        else:
            messages.error(request,
                           "Failed to add stats.")
    else:
        form = BaseballGames()

    template = 'management/add_baseball.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_pitcher(request):
    """ Add a baseball stats to database """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Admin can do that.')
        return redirect(reverse('home'))

    if request.method == "POST":
        form = Pitcher(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added stats!')
            return redirect('add_baseball')
        else:
            messages.error(request,
                           "Failed to add stats.")
    else:
        form = Pitcher()

    template = 'management/add_pitcher.html'

    context = {
        'form': form,
    }

    return render(request, template, context)

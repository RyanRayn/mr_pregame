import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BaseballGame, Pitcher
from datetime import datetime
from sportsipy.nba.teams import Teams as NBATeams
from sportsipy.mlb.teams import Teams as MLBTeams
from .models import BasketballTeamStats, TeamName, Season
from .models import BaseballTeamStats, StartingPitcher


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

    addGame = BaseballGame(request.POST, request.FILES)
    addPitcher = Pitcher(request.POST, request.FILES)

    if request.method == "POST":
        if 'add_game' in request.POST:
            if addGame.is_valid():
                addGame.save()
                messages.success(request, 'Successfully added stats!')
                return redirect(reverse('add_baseball'))
            else:
                messages.error(request,
                               "Failed to add stats.")
        else:
            addGame = BaseballGame()

        if 'add_pitcher' in request.POST:
            if addPitcher.is_valid():
                addPitcher.save()
                messages.success(request, 'Successfully added stats!')
                return redirect(reverse('add_baseball'))
            else:
                messages.error(request,
                               "Failed to add stats.")
        else:
            addPitcher = Pitcher()

    template = 'management/add_baseball.html'

    context = {
        'addPitcher': addPitcher,
        'addGame': addGame
    }

    return render(request, template, context)

import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import BasketballGame
import datetime
from sportsipy.nba.boxscore import Boxscore
from sportsipy.nba.boxscore import Boxscores
from sportsipy.nba.schedule import Schedule
from .models import Team, League, Season, Game


def management(request):
    """ View to return site management page """
    schedule = Schedule('CHI')
    for game in schedule:
        boxscore = game.boxscore
        date = game.date
        date_time_date = datetime.datetime.strptime(date, '%a, %b %d, %Y')
        game_date = date_time_date.strftime('%Y-%m-%d')
        away_total_rebounds = game.boxscore.away_total_rebounds
        print(away_total_rebounds)

        context = {
            'game_date': game_date,
            'boxscore': boxscore,
        }

    return render(request, 'management/management.html',
                  context)


def add_basketball(request):
    """ Add a basketball game to database """
    if request.method == "GET":
        team = request.GET.get('abbreviation')
        game_date = request.GET.get('game_date')

    if request.method == "POST":
        form = BasketballGame(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added game!')
            return redirect(reverse('add_basketball'))
        else:
            messages.error(request,
                           "Failed to add game. Please ensure form is valid.")
    else:
        form = BasketballGame()

    team_auto = Team.objects.filter(league__name='NBA')
    template = 'management/add_basketball.html'
    context = {
        'form': form,
        'team_auto': team_auto,
        'team': team,
        'game_date': game_date,
    }

    return render(request, template, context)

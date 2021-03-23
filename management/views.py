import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import BasketballGame
from datetime import datetime
from sportsipy.nba.boxscore import Boxscores
from sportsipy.nba.teams import Teams
from sportsipy.nba.schedule import Schedule
from .models import Team, League, Season, Game


def management(request):
    """ View to return site management page """

    context = {
    }

    return render(request, 'management/management.html',
                  context)


def add_basketball(request):
    """ Add a basketball game to database """
    if request.method == "GET":
        abbreviation = request.GET.get('abbreviation')

    teams = Teams()
    for team in teams:
        if team.abbreviation == abbreviation:
            name = team.name
            points_for = team.opp_points
            field_goals = team.field_goals
            field_goal_attempts = team.field_goal_attempts
            three_pointers = team.three_point_field_goals
            three_point_attempts = team.three_point_field_goal_attempts
            free_throws = team.free_throws
            free_throw_attempts = team.free_throw_attempts
            offensive_rebounds = team.offensive_rebounds
            defensive_rebounds = team.defensive_rebounds
            assists = team.assists
            steals = team.steals
            blocks = team.blocks
            turnovers = team.turnovers
            personal_fouls = team.personal_fouls

    initial = {
                'name': name,
                'points_for': points_for,
                'field_goals': field_goals,
                'field_goal_attempts': field_goal_attempts,
                'three_pointers': three_pointers,
                'three_point_attempts': three_point_attempts,
                'free_throws': free_throws,
                'free_throw_attempts': free_throw_attempts,
                'offensive_rebounds': offensive_rebounds,
                'defensive_rebounds': defensive_rebounds,
                'assists': assists,
                'steals': steals,
                'blocks': blocks,
                'turnovers': turnovers,
                'personal_fouls': personal_fouls,
            }

    if request.method == "POST":
        form = BasketballGame(request.POST, request.FILES, initial=initial)
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
    }

    return render(request, template, context)

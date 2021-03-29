import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import BasketballGame
from datetime import datetime
from sportsipy.nba.boxscore import Boxscores
from sportsipy.nba.teams import Teams
from sportsipy.nba.schedule import Schedule
from .models import TeamName, League, Season, TeamStats


def management(request):
    """ View to return site management page """

    context = {
    }

    return render(request, 'management/management.html',
                  context)


def add_basketball(request):
    """ Add a basketball game to database """

    team_auto = TeamName.objects.filter(league__name='NBA')
    template = 'management/add_basketball.html'

    context = {
        'team_auto': team_auto,
    }

    return render(request, template, context)


def get_nba_stats(request):
    season_stats = {}
    teams = Teams()
    for team in teams:
        team_stats = TeamStats(
            name=team.name,
            season='',
            points_for=team.points,
            field_goals=team.field_goals,
            field_goal_attempts=team.field_goal_attempts,
            three_pointers=team.three_point_field_goals,
            three_point_attempts=team.three_point_field_goal_attempts,
            free_throws=team.free_throws,
            free_throw_attempts=team.free_throw_attempts,
            offensive_rebounds=team.offensive_rebounds,
            defensive_rebounds=team.defensive_rebounds,
            assists=team.assists,
            steals=team.steals,
            blocks=team.blocks,
            turnovers=team.turnovers,
            personal_fouls=team.personal_fouls,
            games_played=team.games_played,
            points_against=team.opp_points,
            opp_free_throw_attempts=team.opp_free_throw_attempts,
            opp_offensive_rebounds=team.opp_offensive_rebounds,
            opp_defensive_rebounds=team.opp_defensive_rebounds,
            opp_field_goal_percentage=team.opp_field_goal_percentage,
        )
        team_stats.save()
        season_stats = TeamStats.objects.all()

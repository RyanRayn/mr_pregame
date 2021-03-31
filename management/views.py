import requests
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import BasketballGame
from datetime import datetime
from sportsipy.nba.boxscore import Boxscores
from sportsipy.nba.teams import Teams as NBATeams
from sportsipy.mlb.teams import Teams as MLBTeams
from sportsipy.nba.schedule import Schedule
from .models import BasketballTeamStats, BaseballTeamStats


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
    teams = NBATeams()
    for team in teams:
        team_stats = BasketballTeamStats(
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
        season_stats = BasketballTeamStats.objects.all()


def add_baseball(request):
    """ Add a baskeball game to database """

    team_auto = TeamName.objects.filter(league__name='MLB')
    template = 'management/add_baseball.html'

    context = {
        'team_auto': team_auto,
    }

    return render(request, template, context)


def get_mlb_stats(request):
    season_stats = {}
    teams = MLBTeams()
    for team in teams:
        team_stats = BaseballTeamStats(
            name=team.name,
            season='MLB2020',
            wins=team.wins,
            losses=team.losses,
            games_played=team.games,
            home_record=team.home_record,
            away_record=team.away_record,
            runs_allowed_per_game=team.runs_allowed_per_game,
            batting_average=team.batting_average,
            earned_runs_against=team.earned_runs_against,
            hits=team.hits,
            hits_allowed=team.hits_allowed,
            home_runs=team.home_runs,
            home_runs_against=team.home_runs_against,
            record_vs_lefties=team.record_vs_left_handed_pitchers,
            record_vs_righties=team.record_vs_right_handed_pitchers,
            record_vs_500_teams=team.record_vs_teams_over_500,
            record_vs_teams_under_500=team.record_vs_teams_under_500,
            on_base_percentage=team.on_base_percentage,
            run_difference=team.run_difference,
            streak=team.streak,
            total_runs=team.total_runs,
            last_ten=team.last_ten_games_record,
        )
        team_stats.save()
        season_stats = BaseballTeamStats.objects.all()
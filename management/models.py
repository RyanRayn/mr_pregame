from django.db import models


class League(models.Model):
    leagues = (
        ('MLB', ('MLB')),
        ('NBA', ('NBA')),
        ('NCAAB', ('NCAAB')),
        ('NFL', ('NFL')),
    )

    name = models.CharField(
        max_length=10, choices=leagues, null=False, blank=False)

    def __str__(self):
        return self.name


class TeamName(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    abbreviation = models.CharField(max_length=10, null=False, blank=False)
    league = models.ForeignKey(
        'League', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=100, default='')
    teams = models.ManyToManyField('TeamName', max_length=20)

    def __str__(self):
        return self.name


class BasketballTeamStats(models.Model):
    name = models.ForeignKey(
        'TeamName', null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey(
        'Season', null=False, blank=False, on_delete=models.CASCADE)
    record = models.CharField(max_length=10)
    games_played = models.IntegerField()
    points_for = models.IntegerField()
    points_against = models.IntegerField()
    field_goals = models.IntegerField()
    field_goal_attempts = models.IntegerField()
    three_pointers = models.IntegerField()
    three_point_attempts = models.IntegerField()
    free_throws = models.IntegerField()
    free_throw_attempts = models.IntegerField()
    opp_free_throw_attempts = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    opp_offensive_rebounds = models.IntegerField()
    opp_defensive_rebounds = models.IntegerField()
    opp_field_goal_percentage = models.FloatField()
    defensive_rebounds = models.IntegerField()
    assists = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    personal_fouls = models.IntegerField()

    def __str__(self):
        return self.name


class BaseballTeamStats(models.Model):
    name = models.ForeignKey(
        'TeamName', null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey(
        'Season', null=False, blank=False, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    games_played = models.IntegerField()
    home_record = models.CharField(max_length=20)
    away_record = models.CharField(max_length=20)
    runs_allowed_per_game = models.FloatField()
    batting_average = models.FloatField()
    earned_runs_against = models.FloatField()
    hits = models.IntegerField()
    hits_allowed = models.IntegerField()
    home_runs = models.IntegerField()
    home_runs_against = models.IntegerField()
    record_vs_lefties = models.CharField(max_length=20)
    record_vs_righties = models.CharField(max_length=20)
    record_vs_500_teams = models.CharField(max_length=20)
    record_vs_teams_under_500 = models.CharField(max_length=20)
    on_base_percentage = models.FloatField()
    run_difference = models.FloatField()
    streak = models.CharField(max_length=20)
    total_runs = models.IntegerField()
    last_ten = models.CharField(max_length=20)

    def __str__(self):
        return self.name

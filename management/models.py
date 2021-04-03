from django.db import models
import datetime


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
    games_played = models.IntegerField(null=True, blank=True)
    points_for = models.IntegerField(null=True, blank=True)
    points_against = models.IntegerField(null=True, blank=True)
    field_goals = models.IntegerField(null=True, blank=True)
    field_goal_attempts = models.IntegerField(null=True, blank=True)
    three_pointers = models.IntegerField(null=True, blank=True)
    three_point_attempts = models.IntegerField(null=True, blank=True)
    free_throws = models.IntegerField(null=True, blank=True)
    free_throw_attempts = models.IntegerField(null=True, blank=True)
    opp_free_throw_attempts = models.IntegerField(null=True, blank=True)
    offensive_rebounds = models.IntegerField(null=True, blank=True)
    defensive_rebounds = models.IntegerField(null=True, blank=True)
    opp_offensive_rebounds = models.IntegerField(null=True, blank=True)
    opp_defensive_rebounds = models.IntegerField(null=True, blank=True)
    opp_field_goal_percentage = models.FloatField(null=True, blank=True)
    defensive_rebounds = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    steals = models.IntegerField(null=True, blank=True)
    blocks = models.IntegerField(null=True, blank=True)
    turnovers = models.IntegerField(null=True, blank=True)
    personal_fouls = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class BaseballGame(models.Model):
    name = models.ForeignKey('TeamName',
                             null=False, blank=False, on_delete=models.CASCADE)
    nicknames = (
        ('Rays', ('Rays')),
        ('Orioles', ('Orioles')),
        ('BlueJays', ('BlueJays')),
        ('RedSox', ('RedSox')),
        ('Yankees', ('Yankees')),
        ('Tigers', ('Tigers')),
        ('Royals', ('Royals')),
        ('WhiteSox', ('WhiteSox')),
        ('Indians', ('Indians')),
        ('Twins', ('Twins')),
        ('Astros', ('Astros')),
        ('Angels', ('Angels')),
        ('Mariners', ('Mariners')),
        ('Rangers', ('Rangers')),
        ('Athletics', ('Athletics')),
        ('Phillies', ('Phillies')),
        ('Mets', ('Mets')),
        ('Nationals', ('Nationals')),
        ('Braves', ('Braves')),
        ('Marlins', ('Marlins')),
        ('Brewers', ('Brewers')),
        ('Pirates', ('Pirates')),
        ('Cardinals', ('Cardinals')),
        ('Cubs', ('Cubs')),
        ('Reds', ('Reds'))
    )

    nickname = models.CharField(max_length=20,
                                choices=nicknames, default='MLB')
    season = models.ForeignKey('Season',
                               null=False, blank=False,
                               on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    win_home = models.IntegerField(null=True, blank=True)
    loss_home = models.IntegerField(null=True, blank=True)
    win_away = models.IntegerField(null=True, blank=True)
    loss_away = models.IntegerField(null=True, blank=True)
    runs = models.IntegerField(null=True, blank=True)
    runs_allowed = models.IntegerField(null=True, blank=True)
    runs_first_five = models.IntegerField(null=True, blank=True)
    runs_allowed_first_five = models.IntegerField(null=True, blank=True)
    at_bats = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    opponent_at_bats = models.IntegerField(null=True, blank=True)
    hits_allowed = models.IntegerField(null=True, blank=True)
    home_runs = models.IntegerField(null=True, blank=True)
    home_runs_against = models.IntegerField(null=True, blank=True)
    strikeouts = models.IntegerField(null=True, blank=True)
    errors = models.IntegerField(null=True, blank=True)
    bullpen_innings = models.DecimalField(
                                          null=True, blank=True,
                                          max_digits=4, decimal_places=2)
    bullpen_runs = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nickname


class StartingPitcher(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    team = models.ForeignKey('TeamName',
                             null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey('Season',
                               null=False, blank=False,
                               on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    win = models.IntegerField(null=True, blank=True)
    loss = models.IntegerField(null=True, blank=True)
    innings = models.DecimalField(
                                  null=True, blank=True,
                                  max_digits=4, decimal_places=2)
    runs = models.IntegerField(null=True, blank=True)
    runs_first_five = models.IntegerField(null=True, blank=True)
    strikeouts = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    walks = models.IntegerField(null=True, blank=True)
    home_runs = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

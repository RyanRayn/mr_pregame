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


class BaseballTeamStats(models.Model):
    teams = (
        ('Los Angeles Dodgers', ('Los Angeles Dodgers')),
        ('Tampa Bay Rays', ('Tampa Bay Rays')),
        ('San Diego Padres', ('San Diego Padres')),
        ('Minnesota Twins', ('Minnesota Twins')),
        ('Oakland Athletics', ('Oakland Athletics')),
        ('Atlanta Braves', ('Atlanta Braves')),
        ('Chicago White Sox', ('Chicago White Sox')),
        ('Cleveland Indians', ('Cleveland Indians')),
        ('Chicago Cubs', ('Chicago Cubs')),
        ('New York Yankees', ('New York Yankees')),
        ('Toronto Blue Jays', ('Toronto Blue Jays')),
        ('St. Louis Cardinals', ('St. Louis Cardinals')),
        ('Miami Marlins', ('Miami Marlins')),
        ('Cincinnati Reds', ('Cincinnati Reds')),
        ('Houston Astros', ('Houston Astros')),
        ('San Francisco Giants', ('San Francisco Giants')),
        ('Milwaukee Brewers', ('Milwaukee Brewers')),
        ('Philadelphia Phillies', ('Philadelphia Phillies')),
        ('Seattle Mariners', ('Seattle Mariners')),
        ('New York Mets', ('New York Mets')),
        ('Colorado Rockies', ('Colorado Rockies')),
        ('Kansas City Royals', ('Kansas City Royals')),
        ('Los Angeles Angels', ('Los Angeles Angels')),
        ('Washington Nationals', ('Washington Nationals')),
        ('Baltimore Orioles', ('Baltimore Orioles')),
        ('Arizona Diamondbacks', ('Arizona Diamondbacks')),
        ('Boston Red Sox', ('Boston Red Sox')),
        ('Detroit Tigers', ('Detroit Tigers')),
        ('Texas Rangers', ('Texas Rangers')),
        ('Pittsburgh Pirates', ('Pittsburgh Pirates')),
    )

    name = models.ForeignKey('TeamName', choices=teams,
                             null=False, blank=False, on_delete=models.CASCADE)

    seasons = (
        ('MLB2021', ('MLB2021')),
    )

    season = models.ForeignKey('Season', choices=seasons, default='MLB2021',
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
    runs_against_first_five = models.IntegerField(null=True, blank=True)
    at_bats = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    hits_allowed = models.IntegerField(null=True, blank=True)
    home_runs = models.IntegerField(null=True, blank=True)
    home_runs_against = models.IntegerField(null=True, blank=True)
    strikeouts = models.IntegerField(null=True, blank=True)
    errors = models.IntegerField(null=True, blank=True)
    bullpen_innings = models.IntegerField(null=True, blank=True)
    bullpen_runs = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class StartingPitcher(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    teams = (
        ('Los Angeles Dodgers', ('Los Angeles Dodgers')),
        ('Tampa Bay Rays', ('Tampa Bay Rays')),
        ('San Diego Padres', ('San Diego Padres')),
        ('Minnesota Twins', ('Minnesota Twins')),
        ('Oakland Athletics', ('Oakland Athletics')),
        ('Atlanta Braves', ('Atlanta Braves')),
        ('Chicago White Sox', ('Chicago White Sox')),
        ('Cleveland Indians', ('Cleveland Indians')),
        ('Chicago Cubs', ('Chicago Cubs')),
        ('New York Yankees', ('New York Yankees')),
        ('Toronto Blue Jays', ('Toronto Blue Jays')),
        ('St. Louis Cardinals', ('St. Louis Cardinals')),
        ('Miami Marlins', ('Miami Marlins')),
        ('Cincinnati Reds', ('Cincinnati Reds')),
        ('Houston Astros', ('Houston Astros')),
        ('San Francisco Giants', ('San Francisco Giants')),
        ('Milwaukee Brewers', ('Milwaukee Brewers')),
        ('Philadelphia Phillies', ('Philadelphia Phillies')),
        ('Seattle Mariners', ('Seattle Mariners')),
        ('New York Mets', ('New York Mets')),
        ('Colorado Rockies', ('Colorado Rockies')),
        ('Kansas City Royals', ('Kansas City Royals')),
        ('Los Angeles Angels', ('Los Angeles Angels')),
        ('Washington Nationals', ('Washington Nationals')),
        ('Baltimore Orioles', ('Baltimore Orioles')),
        ('Arizona Diamondbacks', ('Arizona Diamondbacks')),
        ('Boston Red Sox', ('Boston Red Sox')),
        ('Detroit Tigers', ('Detroit Tigers')),
        ('Texas Rangers', ('Texas Rangers')),
        ('Pittsburgh Pirates', ('Pittsburgh Pirates')),
    )

    team = models.ForeignKey('TeamName', choices=teams,
                             null=False, blank=False, on_delete=models.CASCADE)
    seasons = (
        ('MLB2021', ('MLB2021')),
    )

    season = models.ForeignKey('Season', choices=seasons, default='MLB2021',
                               null=False, blank=False,
                               on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    win = models.IntegerField()
    loss = models.IntegerField()
    innings = models.IntegerField()
    runs = models.IntegerField()
    runs_first_five = models.IntegerField()
    strikeouts = models.IntegerField()
    hits = models.IntegerField()
    walks = models.IntegerField()
    home_runs = models.IntegerField()

    def __str__(self):
        return self.name

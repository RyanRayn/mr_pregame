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
    twitter_id = models.CharField(max_length=100, default=name)
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


class MLBGame(models.Model):
    name = models.ForeignKey('TeamName',
                             null=False, blank=False, on_delete=models.CASCADE)
    nicknames = (
        ('Angels', ('Angels')),
        ('Astros', ('Astros')),
        ('Athletics', ('Athletics')),
        ('BlueJays', ('BlueJays')),
        ('Braves', ('Braves')),
        ('Brewers', ('Brewers')),
        ('Cardinals', ('Cardinals')),
        ('Cubs', ('Cubs')),
        ('Diamondbacks', ('Diamondbacks')),
        ('Dodgers', ('Dodgers')),
        ('Giants', ('Giants')),
        ('Indians', ('Indians')),
        ('Mariners', ('Mariners')),
        ('Marlins', ('Marlins')),
        ('Mets', ('Mets')),
        ('Nationals', ('Nationals')),
        ('Orioles', ('Orioles')),
        ('Padres', ('Padres')),
        ('Phillies', ('Phillies')),
        ('Pirates', ('Pirates')),
        ('Rangers', ('Rangers')),
        ('Rays', ('Rays')),
        ('Reds', ('Reds')),
        ('RedSox', ('RedSox')),
        ('Rockies', ('Rockies')),
        ('Royals', ('Royals')),
        ('Tigers', ('Tigers')),
        ('Twins', ('Twins')),
        ('WhiteSox', ('WhiteSox')),
        ('Yankees', ('Yankees'))
    )

    nickname = models.CharField(max_length=20,
                                choices=nicknames, default='MLB')
    teams = (
        ('Arizona Diamondbacks', ('Arizona Diamondbacks')),
        ('Atlanta Braves', ('Atlanta Braves')),
        ('Baltimore Orioles', ('Baltimore Orioles')),
        ('Boston Red Sox', ('Boston Red Sox')),
        ('Chicago Cubs', ('Chicago Cubs')),
        ('Chicago White Sox', ('Chicago White Sox')),
        ('Cincinnati Reds', ('Cincinnati Reds')),
        ('Cleveland Indians', ('Cleveland Indians')),
        ('Colorado Rockies', ('Colorado Rockies')),
        ('Detroit Tigers', ('Detroit Tigers')),
        ('Houston Astros', ('Houston Astros')),
        ('Kansas City Royals', ('Kansas City Royals')),
        ('Los Angeles Angels', ('Los Angeles Angels')),
        ('Los Angeles Dodgers', ('Los Angeles Dodgers')),
        ('Miami Marlins', ('Miami Marlins')),
        ('Milwaukee Brewers', ('Milwaukee Brewers')),
        ('Minnesota Twins', ('Minnesota Twins')),
        ('New York Mets', ('New York Mets')),
        ('New York Yankees', ('New York Yankees')),
        ('Oakland Athletics', ('Oakland Athletics')),
        ('Philadelphia Phillies', ('Philadelphia Phillies')),
        ('Pittsburgh Pirates', ('Pittsburgh Pirates')),
        ('San Diego Padres', ('San Diego Padres')),
        ('San Francisco Giants', ('San Francisco Giants')),
        ('Seattle Mariners', ('Seattle Mariners')),
        ('St. Louis Cardinals', ('St. Louis Cardinals')),
        ('Tampa Bay Rays', ('Tampa Bay Rays')),
        ('Texas Rangers', ('Texas Rangers')),
        ('Toronto Blue Jays', ('Toronto Blue Jays')),
        ('Washington Nationals', ('Washington Nationals'))
    )

    opponent = models.CharField(max_length=50, choices=teams, default='MLB')
    season = models.ForeignKey('Season',
                               null=False, blank=False,
                               on_delete=models.CASCADE)
    date = models.DateField()
    win_home = models.IntegerField(null=True, blank=True, default=0)
    loss_home = models.IntegerField(null=True, blank=True, default=0)
    win_away = models.IntegerField(null=True, blank=True, default=0)
    loss_away = models.IntegerField(null=True, blank=True, default=0)
    runs = models.IntegerField(null=True, blank=True, default=0)
    runs_allowed = models.IntegerField(null=True, blank=True, default=0)
    runs_first_five = models.IntegerField(null=True, blank=True, default=0)
    runs_allowed_first_five = models.IntegerField(null=True, blank=True,
                                                  default=0)
    at_bats = models.IntegerField(null=True, blank=True, default=0)
    hits = models.IntegerField(null=True, blank=True, default=0)
    opponent_at_bats = models.IntegerField(null=True, blank=True, default=0)
    hits_allowed = models.IntegerField(null=True, blank=True, default=0)
    home_runs = models.IntegerField(null=True, blank=True, default=0)
    home_runs_against = models.IntegerField(null=True, blank=True, default=0)
    strikeouts = models.IntegerField(null=True, blank=True, default=0)
    errors = models.IntegerField(null=True, blank=True, default=0)
    opponent_errors = models.IntegerField(null=True, blank=True, default=0)
    bullpen_inning_thirds = models.IntegerField(null=True, blank=True,
                                                default=0)
    bullpen_runs = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.nickname


class StartingPitcher(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    team = models.ForeignKey('TeamName',
                             null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey('Season',
                               null=False, blank=False,
                               on_delete=models.CASCADE)
    date = models.DateField()
    win = models.IntegerField(null=True, blank=True, default=0)
    loss = models.IntegerField(null=True, blank=True, default=0)
    inning_thirds = models.IntegerField(null=True, blank=True, default=0)
    runs = models.IntegerField(null=True, blank=True, default=0)
    runs_first_five = models.IntegerField(null=True, blank=True, default=0)
    strikeouts = models.IntegerField(null=True, blank=True, default=0)
    hits = models.IntegerField(null=True, blank=True, default=0)
    walks = models.IntegerField(null=True, blank=True, default=0)
    home_runs = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class MLBGameLine(models.Model):
    gameID = models.IntegerField()
    gamedate = models.DateTimeField()
    gameday = models.DateTimeField(null=True)
    league = models.CharField(max_length=10)
    summary = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    away_abbr = models.CharField(max_length=10)
    home_team = models.CharField(max_length=100)
    home_abbr = models.CharField(max_length=10)
    venue = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    away_spread = models.DecimalField(
        max_digits=4, decimal_places=1, default=0.0)
    away_odds = models.IntegerField(default=0)
    away_moneyline = models.IntegerField(default=0)
    home_spread = models.DecimalField(
        max_digits=4, decimal_places=1, default=0.0)
    home_odds = models.IntegerField(default=0)
    home_moneyline = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    over_odds = models.IntegerField(default=0)
    under_odds = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    current_inning = models.IntegerField(default=0)
    status = models.CharField(max_length=25)
    pick = models.TextField(blank=True)
    pick_type = models.CharField(max_length=100, blank=True)
    away_starter = models.CharField(max_length=100, blank=True)
    home_starter = models.CharField(max_length=100, blank=True)
    away_starter_era = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.00)
    home_starter_era = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.00)
    away_starter_record = models.CharField(max_length=6, blank=True)
    home_starter_record = models.CharField(max_length=6, blank=True)
    away_starter_k = models.IntegerField(default=0)
    home_starter_k = models.IntegerField(default=0)
    away_starter_ip = models.DecimalField(
        max_digits=4, decimal_places=1, default=0.0)
    home_starter_ip = models.DecimalField(
        max_digits=4, decimal_places=1, default=0.0)
    away_starter_hand = models.CharField(max_length=3, blank=True)
    home_starter_hand = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return str(self.summary)

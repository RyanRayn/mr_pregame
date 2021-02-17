from django.db import models


class League(models.Model):
    LEAGUES = (
        ('MLB', ('MLB')),
        ('NBA', ('NBA')),
        ('NCAAB', ('NCAAB')),
        ('NFL', ('NFL')),
    )

    name = models.CharField(
        max_length=10, choices=LEAGUES, null=False, blank=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    abbreviation = models.CharField(max_length=10, null=False, blank=False)
    league = models.ForeignKey(
        'League', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=100, default='')
    teams = models.ManyToManyField('Team', max_length=20)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.ForeignKey(
        'Team', null=False, blank=False, on_delete=models.CASCADE)
    season = models.ForeignKey(
        'Season', null=False, blank=False, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    record = models.CharField(max_length=10)
    opponent = models.CharField(max_length=100)
    points_for = models.IntegerField()
    field_goals = models.IntegerField()
    field_goal_attempts = models.IntegerField()
    three_pointers = models.IntegerField()
    three_point_attempts = models.IntegerField()
    free_throws = models.IntegerField()
    free_throw_attempts = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    assists = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    personal_fouls = models.IntegerField()

    def __str__(self):
        return self.name

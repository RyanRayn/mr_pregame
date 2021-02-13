from django.db import models


class League(models.Model):
    LEAGUES = (
        ('MLB', ('MLB')),
        ('NBA', ('NBA')),
        ('NCAAB', ('NCAAB')),
        ('NFL', ('NFL')),
    )

    name = models.CharField(
        max_length=254,
        choices=LEAGUES,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name


class Teams(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        blank=False
    )

    league = models.ForeignKey(
        'League',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.IntegerField(
        null=False,
        blank=False,
    )

    season = models.ManyToManyField(Teams)

    def __str__(self):
        return self.name


class Games(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        blank=False,
    )

    season = models.ForeignKey(
        'Season',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Stats(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        blank=False,
    )

    game = models.ForeignKey(
        'Games',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

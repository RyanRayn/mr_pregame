# Generated by Django 3.1.5 on 2021-04-10 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_auto_20210405_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseballgame',
            name='opponent_errors',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='baseballgame',
            name='date',
            field=models.DateField(default=datetime.date(2021, 4, 9)),
        ),
        migrations.AlterField(
            model_name='baseballgame',
            name='opponent',
            field=models.CharField(choices=[('Arizona Diamondbacks', 'Arizona Diamondbacks'), ('Atlanta Braves', 'Atlanta Braves'), ('Baltimore Orioles', 'Baltimore Orioles'), ('Boston Red Sox', 'Boston Red Sox'), ('Chicago Cubs', 'Chicago Cubs'), ('Chicago White Sox', 'Chicago White Sox'), ('Cincinnati Reds', 'Cincinnati Reds'), ('Cleveland Indians', 'Cleveland Indians'), ('Colorado Rockies', 'Colorado Rockies'), ('Detroit Tigers', 'Detroit Tigers'), ('Houston Astros', 'Houston Astros'), ('Kansas City Royals', 'Kansas City Royals'), ('Los Angeles Angels', 'Los Angeles Angels'), ('Los Angeles Dodgers', 'Los Angeles Dodgers'), ('Miami Marlins', 'Miami Marlins'), ('Milwaukee Brewers', 'Milwaukee Brewers'), ('Minnesota Twins', 'Minnesota Twins'), ('New York Mets', 'New York Mets'), ('New York Yankees', 'New York Yankees'), ('Oakland Athletics', 'Oakland Athletics'), ('Philadelphia Phillies', 'Philadelphia Phillies'), ('Pittsburgh Pirates', 'Pittsburgh Pirates'), ('San Diego Padres', 'San Diego Padres'), ('San Francisco Giants', 'San Francisco Giants'), ('Seattle Mariners', 'Seattle Mariners'), ('St. Louis Cardinals', 'St. Louis Cardinals'), ('Tampa Bay Rays', 'Tampa Bay Rays'), ('Texas Rangers', 'Texas Rangers'), ('Toronto Blue Jays', 'Toronto Blue Jays'), ('Washington Nationals', 'Washington Nationals')], default='MLB', max_length=50),
        ),
        migrations.AlterField(
            model_name='startingpitcher',
            name='date',
            field=models.DateField(default=datetime.date(2021, 4, 9)),
        ),
    ]

# Generated by Django 3.1.5 on 2021-04-23 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0029_auto_20210418_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlbgameline',
            name='away_starter',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='away_starter_era',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='away_starter_k',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='away_starter_record',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='home_starter',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='home_starter_era',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='home_starter_k',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mlbgameline',
            name='home_starter_record',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='mlbgame',
            name='date',
            field=models.DateField(default=datetime.date(2021, 4, 22)),
        ),
        migrations.AlterField(
            model_name='startingpitcher',
            name='date',
            field=models.DateField(default=datetime.date(2021, 4, 22)),
        ),
    ]

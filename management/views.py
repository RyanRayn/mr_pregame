import requests
import json
from django.shortcuts import render

from datetime import datetime
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.boxscore import Boxscores
from sportsipy.ncaab.schedule import Schedule


def management(request):
    """ View to return site management page """
    team = 'PURDUE'
    team_schedule = Schedule(team)
    schedule = list((team_schedule))

    context = {
        'team': team,
        'schedule': schedule,
    }

    return render(request, 'management/management.html', context)

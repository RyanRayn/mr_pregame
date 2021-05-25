from django.shortcuts import render
from profiles.models import UserProfile
from management.models import MLBGameLine
import datetime
import pytz


def index(request):
    """ View to return index page """
    # Date format to get todays games from Gameline model
    todays_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    date_LA = todays_date.strftime('%B %-d, %Y')
    all_games = MLBGameLine.objects.all()
    profiles = UserProfile.objects.all()

    context = {
        'profiles': profiles,
        'date_LA': date_LA,
        'all_games': all_games,
    }

    return render(request, 'home/index.html', context)

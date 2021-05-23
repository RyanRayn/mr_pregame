from django.shortcuts import render
from profiles.models import UserProfile


def index(request):
    """ View to return index page """

    profiles = UserProfile.objects.all()

    context = {
        'profiles': profiles
    }

    return render(request, 'home/index.html', context)

from django.shortcuts import render


def games(request):
    """ View to return games page """

    return render(request, 'games/games.html')

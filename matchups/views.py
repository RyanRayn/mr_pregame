from django.shortcuts import render


def matchups(request):
    """ a view to show MLB game matchups """

    return render(request, 'matchups/matchups.html')

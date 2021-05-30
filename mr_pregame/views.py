from django.shortcuts import render


def handler404(request, *args, **argv):
    """ View to direct users to custom 404 error page """
    return render(request, '404.html')


def handler500(request, *args, **argv):
    """ View to direct users to custom 500 error page """
    return render(request, '500.html')

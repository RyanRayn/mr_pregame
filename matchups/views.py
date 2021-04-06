from django.shortcuts import render


def matchups(request):
    """ a view to show MLB game matchups """

    if request.method == "GET":
        summary = request.GET.get('summary')
        league = request.GET.get('league')
        homeTeam = request.GET.get('homeTeam')
        awayTeam = request.GET.get('awayTeam')
        date = request.GET.get('date')
        time = request.GET.get('time')
        venue = request.GET.get('venue')
        city = request.GET.get('city')
        state = request.GET.get('state')
        awayAbbr = request.GET.get('awayAbbr')
        homeAbbr = request.GET.get('homeAbbr')
        awaySpread = request.GET.get('awaySpread')
        homeSpread = request.GET.get('homeSpread')
        awayOdds = request.GET.get('awayOdds')
        homeOdds = request.GET.get('homeOdds')
        homeML = request.GET.get('homeML')
        awayML = request.GET.get('awayML')
        total = request.GET.get('total')

    context = {
        'summary': summary,
        'league': league,
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
        'date': date,
        'time': time,
        'venue': venue,
        'city': city,
        'state': state,
        'awayAbbr': awayAbbr,
        'homeAbbr': homeAbbr,
        'awaySpread': awaySpread,
        'homeSpread': homeSpread,
        'awayOdds': awayOdds,
        'homeOdds': homeOdds,
        'homeML': homeML,
        'awayML': awayML,
        'total': total,
    }

    return render(request, 'matchups/matchups.html', context)

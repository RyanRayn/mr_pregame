from django.contrib import admin
from .models import League, TeamName, Season
from .models import BasketballTeamStats, BaseballTeamStats


admin.site.register(League)
admin.site.register(TeamName)
admin.site.register(Season)
admin.site.register(BasketballTeamStats)
admin.site.register(BaseballTeamStats)

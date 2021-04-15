from django.contrib import admin
from .models import League, TeamName, Season, MLBGameLine
from .models import BasketballTeamStats, MLBGame, StartingPitcher


admin.site.register(League)
admin.site.register(TeamName)
admin.site.register(Season)
admin.site.register(BasketballTeamStats)
admin.site.register(MLBGame)
admin.site.register(StartingPitcher)
admin.site.register(MLBGameLine)

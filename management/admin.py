from django.contrib import admin
from .models import League, TeamName, Season, TeamStats


admin.site.register(League)
admin.site.register(TeamName)
admin.site.register(Season)
admin.site.register(TeamStats)

from django.contrib import admin

from .models import *

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(TeamMatchStats)
admin.site.register(NonTeamMatchStats)

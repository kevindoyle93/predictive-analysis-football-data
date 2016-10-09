from django.contrib import admin

from football_data.models import League, Team, Stadium, Player, Match


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league']
    list_filter = ['league']


class StadiumAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'capacity']
    list_filter = ['team__league']


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name']


class MatchAdmin(admin.ModelAdmin):
    list_display = ['date', 'home_team', 'away_team', 'full_time_result']
    list_filter = ['home_team__league']

admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)

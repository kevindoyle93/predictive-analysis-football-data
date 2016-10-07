from django.contrib import admin

from football_data.models import League, Team, Stadium


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league']
    list_filter = ['league']


class StadiumAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'capacity']
    list_filter = ['team__league']

admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium, StadiumAdmin)

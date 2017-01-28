from django.contrib import admin

from football_data.models import League, Team, Stadium, Player, Match, DecisionTreeModel


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
    readonly_fields = [
        'home_player_1',
        'home_player_2',
        'home_player_3',
        'home_player_4',
        'home_player_5',
        'home_player_6',
        'home_player_7',
        'home_player_8',
        'home_player_9',
        'home_player_10',
        'home_player_11',
        'away_player_1',
        'away_player_2',
        'away_player_3',
        'away_player_4',
        'away_player_5',
        'away_player_6',
        'away_player_7',
        'away_player_8',
        'away_player_9',
        'away_player_10',
        'away_player_11',
    ]
    list_filter = ['home_team__league']

admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(DecisionTreeModel)

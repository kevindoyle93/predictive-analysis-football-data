from django.contrib import admin

from football_data.models import League, Team, Match, MachineLearningModel, DataFeature, TrainingDrill


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league']
    list_filter = ['league']


class MatchAdmin(admin.ModelAdmin):
    list_display = ['date', 'home_team', 'away_team', 'full_time_result']
    list_filter = ['home_team__league']


class DataFeatureAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'model', 'is_target_feature', 'positive_weight']
    readonly_fields = ['positive_weight', 'std_dev']


class TrainingDrillAdmin(admin.ModelAdmin):
    list_display = ['name', 'feature']

admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MachineLearningModel)
admin.site.register(DataFeature, DataFeatureAdmin)
admin.site.register(TrainingDrill, TrainingDrillAdmin)

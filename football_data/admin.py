from django.contrib import admin

from football_data.models import League, Team, Match, MachineLearningModel, DataFeature, TrainingDrill, Coach


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']

admin.site.register(League, LeagueAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league']
    list_filter = ['league']

admin.site.register(Team, TeamAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['date', 'home_team', 'away_team', 'full_time_result']
    list_filter = ['home_team__league']

admin.site.register(Match, MatchAdmin)


class DataFeatureAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'model', 'is_target_feature', 'positive_weight']
    readonly_fields = ['positive_weight', 'std_dev']

admin.site.register(DataFeature, DataFeatureAdmin)


class TrainingDrillAdmin(admin.ModelAdmin):
    list_display = ['name', 'feature']

admin.site.register(TrainingDrill, TrainingDrillAdmin)


class CoachAdmin(admin.ModelAdmin):
    list_display = ['username', 'team']

    def username(self, obj):
        return obj.user.username

admin.site.register(Coach, CoachAdmin)

admin.site.register(MachineLearningModel)

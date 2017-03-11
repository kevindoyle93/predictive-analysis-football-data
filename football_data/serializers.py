from rest_framework import serializers

from football_data.models import *


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        default_predictive_model = MachineLearningModel.objects.get(default=True)
        Coach.objects.create(user=user, predictive_model=default_predictive_model)
        return user


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team


class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = [
            'date',
            'home_team',
            'away_team',
            'full_time_home_goals',
            'full_time_away_goals',
            'half_time_home_goals',
            'half_time_away_goals',
            'full_time_result',
            'half_time_result',
            'home_possession',
            'away_possession',
            'home_total_shots',
            'away_total_shots',
            'home_shots_on_target',
            'away_shots_on_target',
            'home_corners',
            'away_corners',
            'home_fouls_committed',
            'away_fouls_committed',
            'home_yellow_cards',
            'away_yellow_cards',
            'home_red_cards',
            'away_red_cards',
        ]


class TeamMatchSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = [
            'date',
            'home_team',
            'away_team',
            'full_time_home_goals',
            'full_time_away_goals',
            'half_time_home_goals',
            'half_time_away_goals',
            'full_time_result',
            'half_time_result',
            'home_possession',
            'away_possession',
            'home_total_shots',
            'away_total_shots',
            'home_shots_on_target',
            'away_shots_on_target',
            'home_corners',
            'away_corners',
            'home_fouls_committed',
            'away_fouls_committed',
            'home_offsides',
            'away_offsides',
            'home_yellow_cards',
            'away_yellow_cards',
            'home_red_cards',
            'away_red_cards',
        ]

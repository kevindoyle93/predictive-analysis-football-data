from rest_framework import serializers

from football_data.models import *


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player


class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()

    # home_player_1 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_2 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_3 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_4 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_5 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_6 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_7 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_8 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_9 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_10 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # home_player_11 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_1 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_2 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_3 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_4 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_5 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_6 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_7 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_8 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_9 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_10 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    # away_player_11 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')

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
            'home_win_average_odds',
            'draw_average_odds',
            'away_win_average_odds',
            'home_win_max_odds',
            'draw_max_odds',
            'away_win_max_odds',
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

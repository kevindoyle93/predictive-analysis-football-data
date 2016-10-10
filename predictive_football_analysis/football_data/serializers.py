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
    home_team = serializers.HyperlinkedRelatedField(read_only=True, view_name='team-detail')
    away_team = serializers.HyperlinkedRelatedField(read_only=True, view_name='team-detail')

    home_player_1 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_2 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_3 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_4 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_5 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_6 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_7 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_8 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_9 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_10 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    home_player_11 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_1 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_2 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_3 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_4 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_5 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_6 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_7 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_8 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_9 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_10 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')
    away_player_11 = serializers.HyperlinkedRelatedField(read_only=True, view_name='player-detail')

    class Meta:
        model = Match

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
    class Meta:
        model = Match

from rest_framework import serializers

from football_data.models import *


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team

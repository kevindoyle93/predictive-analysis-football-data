from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
import django_filters

from football_data.serializers import *
from football_data.models import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'leagues': reverse('league-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'stadiums': reverse('stadium-list', request=request, format=format),
        'players': reverse('player-list', request=request, format=format),
        'matches': reverse('match-list', request=request, format=format),
    })


class LeagueList(generics.ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filter_fields = ('name', )


class LeagueDetail(generics.RetrieveAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class TeamFilter(django_filters.FilterSet):
    league = django_filters.CharFilter(name='league__name')

    class Meta:
        model = Team
        fields = ['name', 'league']


class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_class = TeamFilter


class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class StadiumList(generics.ListAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer


class StadiumDetail(generics.RetrieveAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer


class PlayerList(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class MatchFilter(django_filters.FilterSet):
    home_team = django_filters.CharFilter(name='home_team__name')
    away_team = django_filters.CharFilter(name='away_team__name')

    min_home_possession = django_filters.NumberFilter(name='home_possession', lookup_expr='gte')
    max_home_possession = django_filters.NumberFilter(name='home_possession', lookup_expr='lte')

    class Meta:
        model = Match
        fields = [
            'home_team',
            'away_team',
            'full_time_result',
            'half_time_result',
        ]


class MatchList(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_class = MatchFilter


class MatchDetail(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

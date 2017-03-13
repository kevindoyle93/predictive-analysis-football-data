from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
import django_filters

from django.db.models import Q
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import numpy as np

from football_data.serializers import *
from football_data.permissions import IsCoach
from football_data.models import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'leagues': reverse('league-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'matches': reverse('match-list', request=request, format=format),
        'coaches': reverse('coaches-create', request=request, format=format),
        'app-matches': reverse('app-matches', request=request, format=format),
    })


class CoachCreate(generics.CreateAPIView):
    model = Coach
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


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


class TeamMatchesList(generics.ListAPIView):
    def get_queryset(self):
        team = Team.objects.get(pk=self.kwargs['pk'])
        matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team))
        return matches

    def paginate_queryset(self, queryset):
        return None

    serializer_class = TeamMatchSerializer


class MatchFilter(django_filters.FilterSet):
    league = django_filters.CharFilter(name='home_team__league__name')

    min_date = django_filters.DateTimeFilter(name='date', lookup_expr='gte')
    max_date = django_filters.DateTimeFilter(name='date', lookup_expr='lte')

    home_team = django_filters.CharFilter(name='home_team__name')
    away_team = django_filters.CharFilter(name='away_team__name')

    min_home_full_time_goals = django_filters.NumberFilter(name='full_time_home_goals', lookup_expr='gte')
    max_home_full_time_goals = django_filters.NumberFilter(name='full_time_home_goals', lookup_expr='lte')
    min_away_full_time_goals = django_filters.NumberFilter(name='full_time_away_goals', lookup_expr='gte')
    max_away_full_time_goals = django_filters.NumberFilter(name='full_time_away_goals', lookup_expr='lte')

    min_home_half_time_goals = django_filters.NumberFilter(name='half_time_home_goals', lookup_expr='gte')
    max_home_half_time_goals = django_filters.NumberFilter(name='half_time_home_goals', lookup_expr='lte')
    min_away_half_time_goals = django_filters.NumberFilter(name='half_time_away_goals', lookup_expr='gte')
    max_away_half_time_goals = django_filters.NumberFilter(name='half_time_away_goals', lookup_expr='lte')

    min_home_possession = django_filters.NumberFilter(name='home_possession', lookup_expr='gte')
    max_home_possession = django_filters.NumberFilter(name='home_possession', lookup_expr='lte')
    min_away_possession = django_filters.NumberFilter(name='away_possession', lookup_expr='gte')
    max_away_possession = django_filters.NumberFilter(name='away_possession', lookup_expr='lte')

    min_home_shots = django_filters.NumberFilter(name='home_total_shots', lookup_expr='gte')
    max_home_shots = django_filters.NumberFilter(name='home_total_shots', lookup_expr='lte')
    min_away_shots = django_filters.NumberFilter(name='away_total_shots', lookup_expr='gte')
    max_away_shots = django_filters.NumberFilter(name='away_total_shots', lookup_expr='lte')

    min_home_shots_on_target = django_filters.NumberFilter(name='home_shots_on_target', lookup_expr='gte')
    max_home_shots_on_target = django_filters.NumberFilter(name='home_shots_on_target', lookup_expr='lte')
    min_away_shots_on_target = django_filters.NumberFilter(name='away_shots_on_target', lookup_expr='gte')
    max_away_shots_on_target = django_filters.NumberFilter(name='away_shots_on_target', lookup_expr='lte')

    min_home_corners = django_filters.NumberFilter(name='home_corners', lookup_expr='gte')
    max_home_corners = django_filters.NumberFilter(name='home_corners', lookup_expr='lte')
    min_away_corners = django_filters.NumberFilter(name='away_corners', lookup_expr='gte')
    max_away_corners = django_filters.NumberFilter(name='away_corners', lookup_expr='lte')

    min_home_fouls_committed = django_filters.NumberFilter(name='home_fouls_committed', lookup_expr='gte')
    max_home_fouls_committed = django_filters.NumberFilter(name='home_fouls_committed', lookup_expr='lte')
    min_away_fouls_committed = django_filters.NumberFilter(name='away_fouls_committed', lookup_expr='gte')
    max_away_fouls_committed = django_filters.NumberFilter(name='away_fouls_committed', lookup_expr='lte')

    min_home_yellow_cards = django_filters.NumberFilter(name='home_yellow_cards', lookup_expr='gte')
    max_home_yellow_cards = django_filters.NumberFilter(name='home_yellow_cards', lookup_expr='lte')
    min_away_yellow_cards = django_filters.NumberFilter(name='away_yellow_cards', lookup_expr='gte')
    max_away_yellow_cards = django_filters.NumberFilter(name='away_yellow_cards', lookup_expr='lte')

    min_home_red_cards = django_filters.NumberFilter(name='home_red_cards', lookup_expr='gte')
    max_home_red_cards = django_filters.NumberFilter(name='home_red_cards', lookup_expr='lte')
    min_away_red_cards = django_filters.NumberFilter(name='away_red_cards', lookup_expr='gte')
    max_away_red_cards = django_filters.NumberFilter(name='away_red_cards', lookup_expr='lte')

    class Meta:
        model = Match
        fields = [
            'league',
            'min_date',
            'max_date',
            'home_team',
            'away_team',
            'full_time_result',
            'half_time_result',
            'min_home_full_time_goals',
            'max_home_full_time_goals',
            'min_away_full_time_goals',
            'min_away_full_time_goals',
            'min_home_half_time_goals',
            'max_home_half_time_goals',
            'min_away_half_time_goals',
            'min_away_half_time_goals',
            'min_home_possession',
            'max_home_possession',
            'min_away_possession',
            'max_away_possession',
            'min_home_shots',
            'max_home_shots',
            'min_away_shots',
            'max_away_shots',
            'min_home_shots_on_target',
            'max_home_shots_on_target',
            'min_away_shots_on_target',
            'max_away_shots_on_target',
            'min_home_corners',
            'max_home_corners',
            'min_away_corners',
            'max_away_corners',
            'min_home_fouls_committed',
            'max_home_fouls_committed',
            'min_away_fouls_committed',
            'max_away_fouls_committed',
            'min_home_yellow_cards',
            'max_home_yellow_cards',
            'min_away_yellow_cards',
            'max_away_yellow_cards',
            'min_home_red_cards',
            'max_home_red_cards',
            'min_away_red_cards',
            'max_away_red_cards',
        ]


class MatchList(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_class = MatchFilter


class MatchDetail(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class AppMatchList(generics.ListCreateAPIView):
    serializer_class = AppMatchSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCoach,)

    def get_queryset(self):
        return AppMatch.objects.filter(coach=self.request.user.coach)

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user.coach)


@csrf_exempt
@api_view(['POST'])
def generate_prediction(request):
    ml_model = MachineLearningModel.objects.get(default=True)
    columns = ml_model.training_columns
    column_names = ml_model.descriptive_feature_names

    match_data = [
        column.from_string(request.POST[column.name]) for column in columns
    ]

    # Reshape for Scikit-learn
    match_data = np.array(match_data).reshape(1, -1)

    # Get predictive model from cache and make initial prediction
    model = cache.get(ml_model.algorithm)
    initial_prediction = model.predict_proba(match_data)[0]

    # Get tactical advice from model
    tactical_advice = []
    features_to_alter = ml_model.alterable_features()
    for feature in features_to_alter:
        altered_match_data = np.array(match_data[0]).reshape(1, -1)
        altered_match_data[0][column_names.index(feature.name)] = feature.make_tactical_alteration(altered_match_data[0][column_names.index(feature.name)])

        win_probability = model.predict_proba(altered_match_data)[0][1]
        tactical_advice.append(feature.generate_tactical_advice_card(win_probability, initial_prediction[1]))

    tactical_advice.sort(key=lambda x: x['win_percentage_increase'])

    # Return prediction for now, this will change to returning the tactical suggestion
    data = {
        'result': 'win' if initial_prediction[1] > initial_prediction[0] else 'not-win',
        'win_probability': initial_prediction[1],
        'not_win_probability': initial_prediction[0],
        'tactical_advice': tactical_advice,
    }
    return JsonResponse(data)

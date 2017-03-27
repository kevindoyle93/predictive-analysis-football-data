from datetime import datetime

from rest_framework.test import APITestCase, APIRequestFactory

from football_data.models import League, Team, Match
from football_data.views import TeamMatchesList


class ViewTests(APITestCase):

    base_match_stats = {
        'date': datetime.now(),
        'full_time_home_goals': 0,
        'full_time_away_goals': 0,
        'half_time_home_goals': 0,
        'half_time_away_goals': 0,
        'full_time_result': 'D',
        'half_time_result': 'D',
        'home_possession': '50.0',
        'away_possession': '50.0',
        'home_total_shots': 0,
        'away_total_shots': 0,
        'home_shots_on_target': 0,
        'away_shots_on_target': 0,
        'home_corners': 0,
        'away_corners': 0,
        'home_fouls_committed': 0,
        'away_fouls_committed': 0,
        'home_yellow_cards': 0,
        'away_yellow_cards': 0,
        'home_red_cards': 0,
        'away_red_cards': 0,
    }

    def setUp(self):
        self.league = League.objects.create(name='test league', country='GB')

        self.team_1 = Team.objects.create(name='test team 1', league=self.league)
        self.team_2 = Team.objects.create(name='test team 2', league=self.league)
        self.team_3 = Team.objects.create(name='test team 3', league=self.league)

        Match.objects.create(home_team=self.team_1, away_team=self.team_2, **self.base_match_stats)
        Match.objects.create(home_team=self.team_3, away_team=self.team_1, **self.base_match_stats)
        Match.objects.create(home_team=self.team_2, away_team=self.team_3, **self.base_match_stats)

    def test_team_matches_list(self):
        """
        The TeamMatchesList view should return every match a team was involved in, home or away
        """
        url = 'http://localhost:8000/api/teams/1/matches/'
        view = TeamMatchesList.as_view()

        request = APIRequestFactory().get(url)
        response = view(request, pk=self.team_1.pk)
        self.assertEqual(len(response.data), 2)

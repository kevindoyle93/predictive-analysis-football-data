from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from football_data.models import League, Team, Match, Coach, AppMatch
from football_data.views import TeamMatchesList, AppMatchList


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

    def test_app_match_list_retrieve(self):
        """
        The app match list view should retrieve all and only the matches for the logged in coach
        """
        stats = self.base_match_stats.copy()

        # To fix field name inconsistencies
        stats['home_fouls'] = stats.pop('home_fouls_committed')
        stats['away_fouls'] = stats.pop('away_fouls_committed')
        stats.pop('half_time_result')
        stats.pop('full_time_result')

        coach = Coach.objects.create(user=User.objects.create_user(username='coach', password='pass'))
        AppMatch.objects.create(coach=coach, home_team='home team', away_team='away team', **stats)

        url = reverse('app-match-list')

        self.client.login(username='coach', password='pass')
        res = self.client.get(url)
        self.assertEqual(len(res.json()['results']), 1)
        self.assertEqual(res.json()['results'][0]['coach'], coach.pk)

    def test_app_match_list_create(self):
        """
        The app match create view should assign the logged in coach to a match
        """
        stats = self.base_match_stats.copy()

        # To fix field name inconsistencies
        stats['home_fouls'] = stats.pop('home_fouls_committed')
        stats['away_fouls'] = stats.pop('away_fouls_committed')
        stats['home_team'] = 'home'
        stats['away_team'] = 'away'

        coach = Coach.objects.create(user=User.objects.create_user(username='coach', password='pass'))

        url = reverse('app-match-list')

        self.client.login(username='coach', password='pass')
        res = self.client.post(url, stats)
        print(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['coach'], coach.pk)

from rest_framework import status
from rest_framework.test import APITestCase

from football_data.models import Coach, MachineLearningModel, Match, TrainingDrill, AppMatch


class PredictionServiceTests(APITestCase):
    predictions_url = 'http://localhost:8000/api/get_tactical_advice/'
    registered_predictions_url = 'http://localhost:8000/api/coaches/tactical_advice/'
    coaches_url = 'http://localhost:8000/api/coaches/'
    token_auth_url = 'http://localhost:8000/api/api-token-auth/'

    match_data = {
        'at_home': True,
        'won_match': True,
        'winning_at_half_time': True,
        'half_time_goals': 1,
        'opp_half_time_goals': 0,
        'possession': 50,
        'opp_possession': 50,
        'total_shots': 10,
        'opp_total_shots': 8,
        'shots_on_target': 6,
        'opp_shots_on_target': 3,
        'corners': 5,
        'opp_corners': 4,
        'fouls': 12,
        'opp_fouls': 11,
        'yellow_cards': 2,
        'opp_yellow_cards': 1,
        'red_cards': 0,
        'opp_red_cards': 0
    }

    def setUp(self):
        self.ml_model = MachineLearningModel.objects.create(
            algorithm='LogisticRegression',
            training_data='training_data/individual_teams.csv',
            target_feature_name='won_match',
            default=True,
        )

    def test_anonymous_user_prediction(self):
        """
        Any non-registered user should be able to post a match and receive tactical advice
        """
        response = self.client.post(self.predictions_url, self.match_data)
        results = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tactical_advice', results)
        self.assertIn('win_probability', results)
        self.assertIn('not_win_probability', results)
        self.assertIn('result', results)

    def test_registered_coach_prediction(self):
        """
        When a registered coach requests a prediction, the match data should be persisted
        """
        data = {
            'username': 'testcoach',
            'password': 'testpass',
        }
        # Create Coach
        self.client.post(self.coaches_url, data)

        # Get auth token for coach
        response = self.client.post(self.token_auth_url, data)
        token = response.json()['token']

        # Add the received token to the auth header
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
        response = self.client.post(
            self.predictions_url,
            self.match_data,
            authentication='Token {}'.format(token)
        )
        results = response.json()

        self.assertEqual(AppMatch.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tactical_advice', results)
        self.assertIn('win_probability', results)
        self.assertIn('not_win_probability', results)
        self.assertIn('result', results)

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from football_data.models import Coach, MachineLearningModel


class CoachCreationTests(APITestCase):
    coaches_url = 'http://localhost:8000/api/coaches/'
    token_auth_url = 'http://localhost:8000/api/api-token-auth/'

    def setUp(self):
        MachineLearningModel.objects.create(
            algorithm='LogisticRegression',
            training_data='training_data/individual_teams.csv',
            target_feature_name='won_match',
            default=True,
        )

    def test_token_generated(self):
        """
        A Token should be generated when an Coach is created
        """
        self.assertEqual(Token.objects.count(), 0)

        data = {
            'username': 'testcoach',
            'password': 'testpass',
        }
        response = self.client.post(self.coaches_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Coach.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.get().user, Coach.objects.get().user)

    def test_token_auth(self):
        """
        Once registered, the Coach should be able to make a request to get their Token
        """
        data = {
            'username': 'testcoach',
            'password': 'testpass',
        }

        # Make request to create Coach
        self.client.post(self.coaches_url, data)

        # Make request to get Token
        response = self.client.post(self.token_auth_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')

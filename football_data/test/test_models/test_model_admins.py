from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from football_data.models import Coach
from football_data.admin import CoachAdmin


class MockRequest:
    pass

request = MockRequest()


class ModelAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.ml_model = Coach.objects.create(
            user=User.objects.create_user(username='test', password='pass')
        )

    def test_coach_admin(self):
        """
        The coach admin should display the related user's username
        """
        coach_admin = CoachAdmin(Coach, self.site)
        self.assertEqual(coach_admin.username(Coach.objects.get()), 'test')

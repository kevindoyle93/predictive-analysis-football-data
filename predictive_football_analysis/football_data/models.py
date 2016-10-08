from django.db import models

from django_countries.fields import CountryField
from geopy.distance import distance


class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = CountryField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    league = models.ForeignKey(League, related_name='teams')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['league', 'name']


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    team = models.ForeignKey(Team, related_name='stadiums')
    capacity = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def distance_to(self, opponent_stadium):
        location = (self.lat, self.lng)
        opponent_location = (opponent_stadium.lat, opponent_stadium.lng)
        return distance(location, opponent_location)

    def is_current_stadium(self, match_date):
        if self.end_date is not None:
            if self.start_date is not None:
                return self.end_date > match_date > self.end_date
            return self.end_date > match_date

        return True

    def attendance_percentage(self, attendance):
        return attendance / self.capacity * 100

    class Meta:
        ordering = ['team', 'start_date']


class Player(models.Model):
    name = models.CharField(max_length=100)
    api_id = models.IntegerField(help_text="An ID field used by the Kaggle dataset used in this project")
    date_of_birth = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)


class Match(models.Model):
    date = models.DateTimeField()
    home_team = models.ForeignKey(Team, related_name='home_matches')
    away_team = models.ForeignKey(Team, related_name='away_matches')
    full_time_home_goals = models.PositiveSmallIntegerField()
    full_time_away_goals = models.PositiveSmallIntegerField()
    half_time_home_goals = models.PositiveSmallIntegerField()
    half_time_away_goals = models.PositiveSmallIntegerField()
    full_time_result = models.CharField(
        max_length=1,
        choices=[
            ('H', 'Home win'),
            ('D', 'Draw'),
            ('A', 'Away win')
        ]
    )
    half_time_result = models.CharField(
        max_length=1,
        choices=[
            ('H', 'Home win'),
            ('D', 'Draw'),
            ('A', 'Away win')
        ]
    )

from django.db import models

from django_countries.fields import CountryField
from geopy.distance import distance


class Team(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return self.name


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    team = models.ForeignKey(Team, related_name='stadiums')

    def __str__(self):
        return '{stadium}: {team}'.format(stadium=self.name, team=self.team)

    def distance_to(self, opponent_stadium):
        location = (self.lat, self.lng)
        opponent_location = (opponent_stadium.lat, opponent_stadium.lng)
        return distance(location, opponent_location)


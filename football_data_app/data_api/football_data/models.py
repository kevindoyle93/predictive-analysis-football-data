from django.db import models


class Team(models.Model):
	name = models.CharField(max_length=100)
	venue = models.CharField(max_length=100, null=True, blank=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

	def __str__(self):
		return self.name

class Match(models.Model):
	home_team = models.ForeignKey(Team, related_name="home_matches")
	away_team = models.ForeignKey(Team, related_name="away_matches")
	date = models.DateTimeField()

	def __str__(self):
		return '{h} v {a} {d}'.format(
				h=home_team,
				a=away_team,
				d=date.strftime('%d/%m/%y')
			)


class TeamMatchStats(models.Model):
	team = models.ForeignKey(Team, related_name="match_stats")
	match = models.OneToOneField(Match)
	full_time_goals_count = models.PositiveSmallIntegerField(null=True, blank=True)
	half_time_goals_count = models.PositiveSmallIntegerField(null=True, blank=True)
	full_time_goals_against_count = models.PositiveSmallIntegerField(null=True, blank=True)
	half_time_goals_against_count = models.PositiveSmallIntegerField(null=True, blank=True)
	possession = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)
	total_shots = models.PositiveSmallIntegerField(null=True, blank=True)
	total_shots_allowed = models.PositiveSmallIntegerField(null=True, blank=True)
	shots_on_target = models.PositiveSmallIntegerField(null=True, blank=True)
	shots_on_target_allowed = models.PositiveSmallIntegerField(null=True, blank=True)
	corners_for = models.PositiveSmallIntegerField(null=True, blank=True)
	corners_against = models.PositiveSmallIntegerField(null=True, blank=True)
	offsides_committed = models.PositiveSmallIntegerField(null=True, blank=True)
	offsides_received = models.PositiveSmallIntegerField(null=True, blank=True)
	tackles = models.PositiveSmallIntegerField(null=True, blank=True)
	interceptions = models.PositiveSmallIntegerField(null=True, blank=True)
	interceptions_againts = models.PositiveSmallIntegerField(null=True, blank=True)
	fouls_committed = models.PositiveSmallIntegerField(null=True, blank=True)
	fouls_against = models.PositiveSmallIntegerField(null=True, blank=True)
	yellow_cards = models.PositiveSmallIntegerField(null=True, blank=True)
	red_cards = models.PositiveSmallIntegerField(null=True, blank=True)


class NonTeamMatchStats(models.Model):
	temperature = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)
	wind_speed = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)
	attendance = models.PositiveSmallIntegerField(null=True, blank=True)

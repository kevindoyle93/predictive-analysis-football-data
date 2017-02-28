from django.db import models
from django.core.cache import cache

from django_countries.fields import CountryField
from geopy.distance import distance
from sklearn import tree
import pandas as pd

from football_data.constants import MACHINE_LEARNING_ALGORITHM_CHOICES, MACHINE_LEARNING_ALGORITHMS


class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = CountryField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    league = models.ForeignKey(League, related_name='teams')
    kaggle_api_id = models.IntegerField()

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
    kaggle_api_id = models.IntegerField(help_text="An ID field used by the Kaggle dataset used in this project")
    date_of_birth = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    has_played_match = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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

    # Stats
    home_possession = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    away_possession = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    home_total_shots = models.PositiveSmallIntegerField()
    away_total_shots = models.PositiveSmallIntegerField()
    home_shots_on_target = models.PositiveSmallIntegerField()
    away_shots_on_target = models.PositiveSmallIntegerField()
    home_corners = models.PositiveSmallIntegerField()
    away_corners = models.PositiveSmallIntegerField()
    home_fouls_committed = models.PositiveSmallIntegerField()
    away_fouls_committed = models.PositiveSmallIntegerField()
    home_offsides = models.PositiveSmallIntegerField(null=True, blank=True)
    away_offsides = models.PositiveSmallIntegerField(null=True, blank=True)
    home_yellow_cards = models.PositiveSmallIntegerField()
    away_yellow_cards = models.PositiveSmallIntegerField()
    home_red_cards = models.PositiveSmallIntegerField()
    away_red_cards = models.PositiveSmallIntegerField()

    # Home Lineup
    home_player_1 = models.ForeignKey(Player, related_name='home_matches_p1', null=True, blank=True, editable=False)
    home_player_2 = models.ForeignKey(Player, related_name='home_matches_p2', null=True, blank=True, editable=False)
    home_player_3 = models.ForeignKey(Player, related_name='home_matches_p3', null=True, blank=True, editable=False)
    home_player_4 = models.ForeignKey(Player, related_name='home_matches_p4', null=True, blank=True, editable=False)
    home_player_5 = models.ForeignKey(Player, related_name='home_matches_p5', null=True, blank=True, editable=False)
    home_player_6 = models.ForeignKey(Player, related_name='home_matches_p6', null=True, blank=True, editable=False)
    home_player_7 = models.ForeignKey(Player, related_name='home_matches_p7', null=True, blank=True, editable=False)
    home_player_8 = models.ForeignKey(Player, related_name='home_matches_p8', null=True, blank=True, editable=False)
    home_player_9 = models.ForeignKey(Player, related_name='home_matches_p9', null=True, blank=True, editable=False)
    home_player_10 = models.ForeignKey(Player, related_name='home_matches_p10', null=True, blank=True, editable=False)
    home_player_11 = models.ForeignKey(Player, related_name='home_matches_p11', null=True, blank=True, editable=False)

    home_player_1_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_2_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_3_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_4_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_5_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_6_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_7_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_8_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_9_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_10_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    home_player_11_pos = models.PositiveSmallIntegerField(blank=True, null=True)

    # Away Lineup
    away_player_1 = models.ForeignKey(Player, related_name='away_matches_p1', null=True, blank=True, editable=False)
    away_player_2 = models.ForeignKey(Player, related_name='away_matches_p2', null=True, blank=True, editable=False)
    away_player_3 = models.ForeignKey(Player, related_name='away_matches_p3', null=True, blank=True, editable=False)
    away_player_4 = models.ForeignKey(Player, related_name='away_matches_p4', null=True, blank=True, editable=False)
    away_player_5 = models.ForeignKey(Player, related_name='away_matches_p5', null=True, blank=True, editable=False)
    away_player_6 = models.ForeignKey(Player, related_name='away_matches_p6', null=True, blank=True, editable=False)
    away_player_7 = models.ForeignKey(Player, related_name='away_matches_p7', null=True, blank=True, editable=False)
    away_player_8 = models.ForeignKey(Player, related_name='away_matches_p8', null=True, blank=True, editable=False)
    away_player_9 = models.ForeignKey(Player, related_name='away_matches_p9', null=True, blank=True, editable=False)
    away_player_10 = models.ForeignKey(Player, related_name='away_matches_p10', null=True, blank=True, editable=False)
    away_player_11 = models.ForeignKey(Player, related_name='away_matches_p11', null=True, blank=True, editable=False)

    away_player_1_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_2_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_3_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_4_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_5_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_6_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_7_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_8_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_9_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_10_pos = models.PositiveSmallIntegerField(blank=True, null=True)
    away_player_11_pos = models.PositiveSmallIntegerField(blank=True, null=True)

    home_win_average_odds = models.FloatField(blank=True, null=True)
    draw_average_odds = models.FloatField(blank=True, null=True)
    away_win_average_odds = models.FloatField(blank=True, null=True)
    home_win_max_odds = models.FloatField(blank=True, null=True)
    draw_max_odds = models.FloatField(blank=True, null=True)
    away_win_max_odds = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{h} v {a}'.format(h=self.home_team, a=self.away_team)

    class Meta:
        verbose_name_plural = 'Matches'


class PredictiveModel(models.Model):
    name = models.CharField(max_length=100)
    algorithm = models.CharField(max_length=100)

    model = None

    @property
    def model(self):
        return self.model


class DecisionTreeModel(PredictiveModel):
    model = tree.DecisionTreeClassifier()


class Sport(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MachineLearningModel(models.Model):
    algorithm = models.CharField(max_length=50, choices=MACHINE_LEARNING_ALGORITHM_CHOICES)
    sport = models.ForeignKey(to=Sport, related_name='models')
    training_data = models.FileField(upload_to='training_data'.format(sport.name))
    target_feature_name = models.CharField(max_length=60, help_text='The name of the target feature column as it appears in the training data')

    @property
    def model(self):
        return MACHINE_LEARNING_ALGORITHMS[self.algorithm]

    @property
    def training_columns(self):
        return self.features.filter(is_target_feature=False).order_by('column_index')

    @property
    def descriptive_feature_names(self):
        return [column.name for column in self.training_columns]

    @property
    def target_column(self):
        return self.features.get(is_target_feature=True).name

    def train(self):
        training_data = pd.read_csv(self.training_data.path, index_col=0)
        training_columns = list(training_data.columns)

        target_feature_index = training_columns.index(self.target_feature_name) + 1
        training_column_indexes = [i + 1 for i in range(0, len(training_columns)) if i + 1 != target_feature_index]

        training_columns.remove(self.target_feature_name)

        model = self.model
        model.fit(training_data[training_columns], training_data[self.target_feature_name])

        # Create records for the descriptive features
        weights = model.coef_[0]
        for i in range(0, len(training_columns)):
            feature, created = DataFeature.objects.get_or_create(
                model=self,
                name=training_columns[i],
                display_name=training_columns[i],
                column_index=training_column_indexes[i],
                is_target_feature=False,
                data_type=training_data[training_columns[i]].dtype.name,
                defaults={
                    'positive_weight': weights[i] >= 0,
                    'mean': training_data[training_columns[i]].mean(),
                    'std_dev': training_data[training_columns[i]].std(),
                }
            )
            feature.save()

        # Create a record for the target feature
        feature, created = DataFeature.objects.get_or_create(
            model=self,
            name=self.target_feature_name,
            display_name=self.target_feature_name,
            column_index=target_feature_index,
            is_target_feature=True,
            defaults={
                'mean': training_data[self.target_feature_name].mean(),
                'std_dev': training_data[self.target_feature_name].std(),
                'data_type': training_data[self.target_feature_name].dtype.name,
            }
        )
        feature.save()

        return model

    def alterable_features(self):
        return self.features.annotate(drill_count=models.Count('training_drills')).filter(drill_count__gte=1)

    def save(self, *args, **kwargs):
        super(MachineLearningModel, self).save(*args, **kwargs)
        cache.set(self.algorithm, self.train())

    def __str__(self):
        return self.algorithm


class DataFeature(models.Model):
    DATA_TYPE_CHOICES = (
        ('bool', 'Boolean'),
        ('float64', 'Float'),
        ('int64', 'Integer'),
    )

    display_name = models.CharField(max_length=40, help_text='The readable name of this feature', blank=True, null=True)
    name = models.CharField(max_length=50, help_text='The name as it appears in the dataset')
    model = models.ForeignKey(to=MachineLearningModel, related_name='features')
    column_index = models.IntegerField(help_text='The column index for this feature in the training data (1-indexed)')
    is_target_feature = models.BooleanField(default=False)
    data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICES)

    positive_weight = models.NullBooleanField()
    mean = models.FloatField(default=0)
    std_dev = models.FloatField(default=0)

    def from_string(self, value):
        if self.data_type == 'bool':
            return bool(value)
        elif self.data_type == 'float64':
            return float(value)
        elif self.data_type == 'int64':
            return int(value)

    def generate_tactical_advice_card(self, value, initial_probability):
        title = '{} {}'.format(
            'Increase' if self.positive_weight else 'Decrease',
            self.display_name
        )

        body = 'Increases probability of a win by {} to {}'.format(
            format(value - initial_probability, '.2f'),
            format(value, '.2f'),
        )

        drills = [{'name': drill.name, 'description': drill.description} for drill in self.training_drills.all()]

        return {
            'title': title,
            'body': body,
            'drills': drills
        }

    def make_tactical_alteration(self, value):
        if value < self.mean:
            alteration = self.mean / 2
        else:
            alteration = self.mean / 6

        altered_value = value + alteration if self.positive_weight else value - alteration

        if self.data_type == 'int64':
            return int(altered_value)

        return altered_value

    def __str__(self):
        return '{}: {}'.format(self.display_name, self.model.sport)

    class Meta:
        unique_together = ('model', 'column_index')


class TrainingDrill(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    sport = models.ForeignKey(to=Sport, related_name='training_drills')
    feature = models.ForeignKey(to=DataFeature, related_name='training_drills')

    def __str__(self):
        return self.name

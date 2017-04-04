import pickle

from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token
from picklefield.fields import PickledObjectField
from django_countries.fields import CountryField
import pandas as pd
from scipy.stats import norm

from football_data.constants import MACHINE_LEARNING_ALGORITHM_CHOICES, MACHINE_LEARNING_ALGORITHMS


class MachineLearningModel(models.Model):
    algorithm = models.CharField(max_length=50, choices=MACHINE_LEARNING_ALGORITHM_CHOICES)
    training_data = models.FileField(upload_to='training_data')
    target_feature_name = models.CharField(max_length=60, help_text='The name of the target feature column as it '
                                                                    'appears in the training data')
    default = models.BooleanField(default=False, help_text='Is this the default model? (There can only be one)')
    pickled_model = PickledObjectField(editable=False, null=True, blank=True)

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

    def get_predictive_model(self):
        if cache.get(self.algorithm) is not None:
            return cache.get(self.algorithm)
        else:
            return pickle.loads(self.trained_model.trained_model)

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
                    'min_alteration': max(training_data[training_columns[i]].mean() / 10, 1),
                    'max_alteration': max(training_data[training_columns[i]].std() * 2, 2),
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
                'min_alteration': max(training_data[self.target_feature_name].mean() / 10, 1),
                'max_alteration': max(training_data[self.target_feature_name].std() * 2, 2),
            }
        )
        feature.save()

        return model

    def alterable_features(self):
        return self.features.annotate(drill_count=models.Count('training_drills')).filter(drill_count__gte=1)

    def save(self, *args, **kwargs):
        super(MachineLearningModel, self).save(*args, **kwargs)
        trained_model = self.train()
        TrainedModels.objects.create(ml_algorithm=self, trained_model=pickle.dumps(trained_model))
        cache.set(self.algorithm, trained_model)

    def __str__(self):
        return self.algorithm


class TrainedModels(models.Model):
    ml_algorithm = models.OneToOneField(MachineLearningModel, related_name='trained_model')
    trained_model = PickledObjectField()


class DataFeature(models.Model):
    """
    Column of an Analytics Base Table (ABT)

    Data features are automatically added when a model is trained.
    """
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
    min_alteration = models.FloatField(default=0, help_text='The minimum achievable alteration for this feature')
    max_alteration = models.FloatField(default=0, help_text='The maximum achievable alteration for this feature')

    message = models.TextField(blank=None, null=True, help_text='Why does improving this stat help a team?')

    def from_string(self, value):
        if self.data_type == 'bool':
            return bool(value)
        elif self.data_type == 'float64':
            return float(value)
        elif self.data_type == 'int64':
            return int(value)

    def generate_tactical_advice_card(self, value, initial_probability, alteration):
        win_percentage_increase = (value - initial_probability) * 100

        title = '{} {} by {}'.format(
            'Increase' if self.positive_weight else 'Decrease',
            self.display_name,
            alteration if type(alteration) == int else format(alteration, '.2f'),
        )

        body = 'Increases probability of a win by {}% to {}%'.format(
            format(win_percentage_increase, '.2f'),
            format(value * 100, '.2f'),
        )

        detail = self.message

        drills = [
            {'id': drill.id, 'name': drill.name, 'description': drill.description, 'link': drill.link}
            for drill in self.training_drills.all()
        ]

        return {
            'title': title,
            'feature': self.display_name,
            'body': body,
            'detail': detail,
            'drills': drills,
            'win_percentage_increase': win_percentage_increase
        }

    def make_tactical_alteration(self, value):
        """
        Make a viable alteration to the value of a data feature

        The magnitude of the alteration to a feature value must be viable. Tactical advice can only
        be suitable if the changes being suggested are actually achievable.

        The alteration is calculated based on the probability density function (pdf) for the current data feature.
        The standard deviation is used as a base for achievable alterations and is transformed to an alteration value
        by raising it to the power of the pdf of the value param. This ensures the highest alteration values occur
        when the value param is closest to the mean, with alteration values getting lower as the value param moves
        away from the mean.

        This achieves the effect of providing more achievable alterations to teams performing poorly (i.e. a value
        param significantly lower than the mean), and limiting the alterations for teams that are already performing
        very well (i.e. a value param significantly higher than the mean).

        :param value: the value for this feature of the instance being altered
        :return: the altered value for this feature, and the alteration made
        """

        alterations_distribution = norm(self.mean, self.std_dev)
        pdf_value = alterations_distribution.pdf(value) * 10
        alteration = self.std_dev ** pdf_value

        # Clamp the alteration between the min and max
        alteration = max(min(alteration, self.max_alteration), self.min_alteration)

        altered_value = value + alteration if self.positive_weight else value - alteration

        if self.data_type == 'int64':
            return int(altered_value), int(alteration)

        return altered_value, alteration

    def __str__(self):
        return '{}: {}'.format(self.display_name, self.model)

    class Meta:
        unique_together = ('model', 'column_index')


class TrainingDrill(models.Model):
    """
    A usable drill a coach could add to a training session.

    Each drill is related to a particular sport and data feature.
    The feature field tells the coach which feature of the predictive model would be improved
    by implementing this drill.

    """

    name = models.CharField(max_length=70)
    description = models.TextField()
    link = models.URLField(null=True, blank=True)
    feature = models.ForeignKey(to=DataFeature, related_name='training_drills')

    def __str__(self):
        return self.name


class Coach(models.Model):
    user = models.OneToOneField(User)
    predictive_model = models.ForeignKey(MachineLearningModel, blank=True, null=True)

    @property
    def get_predictive_model(self):
        return cache.get('{}:{}'.format(self.user.username, self.predictive_model.algorithm))

    def __str__(self):
        return self.user.username


# Receiver to create an auth token whenever a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = CountryField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    league = models.ForeignKey(League, related_name='teams', blank=True, null=True)
    coach = models.OneToOneField(Coach, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['league', 'name']


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
    home_yellow_cards = models.PositiveSmallIntegerField()
    away_yellow_cards = models.PositiveSmallIntegerField()
    home_red_cards = models.PositiveSmallIntegerField()
    away_red_cards = models.PositiveSmallIntegerField()

    training_data = models.BooleanField(default=False)

    def __str__(self):
        return '{h} v {a}'.format(h=self.home_team, a=self.away_team)

    class Meta:
        verbose_name_plural = 'Matches'


class AppMatch(models.Model):
    coach = models.ForeignKey(Coach, related_name='matches')
    coach_team_is_home_team = models.BooleanField(default=True)
    date = models.DateTimeField()
    home_team = models.CharField(max_length=30)
    away_team = models.CharField(max_length=30)
    full_time_home_goals = models.PositiveSmallIntegerField()
    full_time_away_goals = models.PositiveSmallIntegerField()
    half_time_home_goals = models.PositiveSmallIntegerField()
    half_time_away_goals = models.PositiveSmallIntegerField()

    # Stats
    home_possession = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    away_possession = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    home_total_shots = models.PositiveSmallIntegerField()
    away_total_shots = models.PositiveSmallIntegerField()
    home_shots_on_target = models.PositiveSmallIntegerField()
    away_shots_on_target = models.PositiveSmallIntegerField()
    home_corners = models.PositiveSmallIntegerField()
    away_corners = models.PositiveSmallIntegerField()
    home_fouls = models.PositiveSmallIntegerField()
    away_fouls = models.PositiveSmallIntegerField()
    home_yellow_cards = models.PositiveSmallIntegerField()
    away_yellow_cards = models.PositiveSmallIntegerField()
    home_red_cards = models.PositiveSmallIntegerField()
    away_red_cards = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} v {}'.format(self.home_team, self.away_team)

    class Meta:
        verbose_name_plural = 'Matches'

from django.apps import AppConfig
from django.core.cache import cache

from football_data.scripts import train_ml_models

DECISION_TREE = 'decision_tree'


class FootballDataConfig(AppConfig):
    name = 'football_data'

    def ready(self):
        """
        The first time the app is run, the predictive models must be trained and cached
        """

        self.create_decision_tree()

    @staticmethod
    def create_decision_tree():
        """
        Initialises and trains a Scikit-lean decision tree model
        """
        models = train_ml_models.create_models()

        for name, model in models.items():
            cache.set(name, model)

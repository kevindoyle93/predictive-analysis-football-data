from django.apps import AppConfig
from django.core.cache import cache

from football_data.scripts import train_ml_models


class FootballDataConfig(AppConfig):
    name = 'football_data'

    def ready(self):
        models = train_ml_models.create_models()

        for name, model in models.items():
            cache.set(name, model)

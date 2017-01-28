from django.apps import AppConfig
from django.core.cache import cache

import pandas as pd
from sklearn import tree, preprocessing

DECISION_TREE = 'decision_tree'


class FootballDataConfig(AppConfig):
    name = 'football_data'

    def ready(self):
        """
        The first time the app is run, the predictive models must be trained and cached
        """

        df = pd.read_csv('football_data/raw_data/abt.csv')

        le_result = preprocessing.LabelEncoder()
        le_result.fit(df['full_time_result'])
        df['full_time_result'] = le_result.transform(df['full_time_result'])
        df['half_time_result'] = le_result.transform(df['half_time_result'])

        d_tree = self.create_decision_tree(df)
        cache.set(DECISION_TREE, d_tree, 0)

    def create_decision_tree(self, df):
        """
        Initialises and trains a Scikit-lean decision tree model
        :param df: pandas DataFrame object with which to train the model
        """

        classifier = tree.DecisionTreeClassifier()
        training_columns = df.columns.values[1:]
        training_features = df[training_columns]
        target_feature = df[df.columns.values[0]]

        classifier.fit(training_features, target_feature)

        return classifier

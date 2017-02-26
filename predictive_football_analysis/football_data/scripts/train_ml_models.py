import pandas as pd

from sklearn import preprocessing
from sklearn import tree

columns = [
        'won_match',
        'at_home',
        'winning_at_half_time',
        'possession',
        'opp_possession',
        'total_shots',
        'opp_total_shots',
        'shots_on_target',
        'opp_shots_on_target',
        'corners',
        'opp_corners',
        'fouls',
        'opp_fouls',
        'yellow_cards',
        'opp_yellow_cards',
        'red_cards',
        'opp_red_cards',
    ]


def create_data_frame():
    return pd.read_csv('football_data/scripts/individual_teams.csv')


def create_decision_tree(training_features, target_feature):
    decision_tree = tree.DecisionTreeClassifier()
    return decision_tree.fit(training_features, target_feature)


def create_models():
    df = create_data_frame()

    training_columns = columns[1:]
    training_features = df[training_columns]
    target_feature = df[columns[0]]

    return {
        'decision_tree': create_decision_tree(training_features, target_feature)
    }

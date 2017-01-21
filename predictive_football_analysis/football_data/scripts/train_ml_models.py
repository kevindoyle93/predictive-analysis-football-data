import pandas as pd

from sklearn import preprocessing
from sklearn import tree

columns = [
        'full_time_result',
        'half_time_result',
        'half_time_home_goals',
        'half_time_away_goals',
        'home_possession',
        'away_possession',
        'home_total_shots',
        'away_total_shots',
        'home_shots_on_target',
        'away_shots_on_target',
        'home_corners',
        'away_corners',
        'home_fouls_committed',
        'away_fouls_committed',
        'home_yellow_cards',
        'away_yellow_cards',
        'home_red_cards',
        'away_red_cards',
    ]


def create_data_frame():
    return pd.read_csv('football_data/scripts/training_data.csv')


def create_decision_tree(training_features, target_feature):
    decision_tree = tree.DecisionTreeClassifier()
    return decision_tree.fit(training_features, target_feature)


def create_models():
    df = create_data_frame()

    # Pre-process string data
    le_result = preprocessing.LabelEncoder()
    le_result.fit(df['full_time_result'])
    df['full_time_result'] = le_result.transform(df['full_time_result'])
    df['half_time_result'] = le_result.transform(df['half_time_result'])

    training_columns = columns[1:]
    training_features = df[training_columns]
    target_feature = df[columns[0]]

    return {
        'decision_tree': create_decision_tree(training_features, target_feature)
    }

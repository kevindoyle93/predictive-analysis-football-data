import pandas as pd

from sklearn import linear_model

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


def create_logistic_regression_model(training_features, target_feature):
    model = linear_model.LogisticRegression(solver='lbfgs')
    return model.fit(training_features, target_feature)


def create_models():
    df = create_data_frame()

    training_columns = columns[1:]
    training_features = df[training_columns]
    target_feature = df[columns[0]]

    return {
        'logistic_regression': create_logistic_regression_model(training_features, target_feature)
    }

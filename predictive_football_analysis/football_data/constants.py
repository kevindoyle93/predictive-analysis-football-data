from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

LOGISTIC_REGRESSION = 'LogisticRegression'
GRADIENT_BOOSTING = 'GradientBoosting'

MACHINE_LEARNING_ALGORITHM_CHOICES = [
    (LOGISTIC_REGRESSION, LOGISTIC_REGRESSION),
    (GRADIENT_BOOSTING, GRADIENT_BOOSTING),
]

MACHINE_LEARNING_ALGORITHMS = {
    LOGISTIC_REGRESSION: LogisticRegression(solver='lbfgs'),
    GRADIENT_BOOSTING: GradientBoostingClassifier(),
}

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm

LOGISTIC_REGRESSION = 'LogisticRegression'
GRADIENT_BOOSTING = 'GradientBoosting'
SVM = 'SVM'

MACHINE_LEARNING_ALGORITHM_CHOICES = [
    (LOGISTIC_REGRESSION, LOGISTIC_REGRESSION),
    # (GRADIENT_BOOSTING, GRADIENT_BOOSTING),
    (SVM, SVM),
]

MACHINE_LEARNING_ALGORITHMS = {
    LOGISTIC_REGRESSION: LogisticRegression(solver='lbfgs'),
    # GRADIENT_BOOSTING: GradientBoostingClassifier(),
    SVM: svm.SVC(kernel='linear', probability=True),
}

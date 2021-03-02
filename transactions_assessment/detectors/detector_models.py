from transactions_assessment.detectors import Detector
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline
import logging


class RFDetector(Detector):
    logger = logging.getLogger('RFDetector')

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(bootstrap=True, n_estimators=500))
    ])

    param_grid = {'rf__n_estimators': [50, 100, 200, 500],
                  'rf__max_depth': [None, 10, 30, 50, 70, 100],
                  'rf__min_samples_split': [2, 4, 8],
                  'rf__max_features': ['sqrt', 'auto'],
                  'rf__max_samples': [.1, .5]
                  }

    def use_bootstrap(self, max_samples: float):
        """
        retrieve current params from random
        forest and add on max samples param
        and set bootstrap to True.
        Feed the updated params_dict back
        into the pipeline

        PARAMS
        --------
        max_samples: float
            the percentage of the data to use
            for each estimator
        """
        params_dict = self.pipe.get_params()
        params_dict['rf__max_samples'] = max_samples
        self.pipe.set_params(**params_dict)

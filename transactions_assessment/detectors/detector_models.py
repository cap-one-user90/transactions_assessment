from transactions_assessment.detectors import Detector
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


class RFDetector(Detector):
    pipe = make_pipeline(StandardScaler(), RandomForestClassifier())

    param_grid = {'randomforestclassifier__n_estimators': [50, 100, 200],
                  'randomforestclassifier__max_depth': [None, 10, 30, 50, 70, 100],
                  'randomforestclassifier__min_samples_split': [2, 4, 8],
                  'randomforestclassifier__max_features': ['sqrt', 'auto']
                  }

    def inject_params(self, model_params: dict):
        """
        input a dictionary of parameters to be
        used in the model pipeline

        PARAMS
        -----------
        model_params: dict
            dictionary of model parameters
        """
        self.pipe = make_pipeline(StandardScaler(), RandomForestClassifier(**model_params))

from sklearn.metrics import classification_report, plot_confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from imblearn.over_sampling import RandomOverSampler
import matplotlib.pyplot as plt
from abc import ABC


class Detector(ABC):

    @property
    def logger(self):
        raise NotImplementedError

    @property
    def pipe(self):
        raise NotImplementedError

    @property
    def param_grid(self):
        raise NotImplementedError

    def set_samples(self,  sampling_strategy=None):
        """
        use over-sampling to duplicate rows of minority
        class

        PARAMS
        ----------
        sampling_strategy: str
            sampling strategy to use. 'minority'
            can be used to sample from minority
            class until numbers are even between
            classes. otherwise use values between
            0 and 1
        """
        if sampling_strategy:
            self.pipe.steps.insert(0, ['sampler', RandomOverSampler(sampling_strategy=sampling_strategy)])

    def train(self, data, labels):
        """
        fit the model
        """
        self.logger.info('Training model..')
        self.pipe.fit(data, labels)
        self.logger.info('Model training complete.')

    def print_score(self, train_data, train_labels, test_data, test_labels):
        """
        print train, test and oob score
        (if available) from a fitted model
        """
        train_score = self.pipe.score(train_data, train_labels)
        test_score = self.pipe.score(test_data, test_labels)
        print(f'train score: {train_score} test score: {test_score}')

    def print_confusion(self, data, labels):
        """
        print the confusion matrix for
        a fitted model
        """
        predictions = self.pipe.predict(data)
        con_report = classification_report(labels, predictions)
        print(con_report)

    def plot_confusion(self, data, labels):
        plot_confusion_matrix(self.pipe, data, labels, cmap=plt.cm.summer)
        plt.show()

    def grid_search(self, data, labels, n_iter=50, cv=3):
        """
        find best hyper-parameters
        """
        grid = RandomizedSearchCV(self.pipe, param_distributions=self.param_grid, n_iter=n_iter,
                                  cv=cv, scoring='f1_macro', refit='f1_macro')
        grid.fit(data, labels)
        print(f'best params: {grid.best_params_} \n best score: {grid.best_score_}')

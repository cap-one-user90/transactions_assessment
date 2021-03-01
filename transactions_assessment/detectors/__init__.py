from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from imblearn.over_sampling import RandomOverSampler
import matplotlib.pyplot as plt
from abc import ABC


class Detector(ABC):

    @property
    def pipe(self):
        raise NotImplementedError

    @property
    def param_grid(self):
        raise NotImplementedError

    def set_samples(self, data, labels, sampling_strategy=0.5):
        """
        set the sample size
        """
        sampler = RandomOverSampler(sampling_strategy=sampling_strategy)
        x_sample, y_sample = sampler.fit_resample(data, labels)
        return x_sample, y_sample

    def train(self, data, labels):
        """
        fit the model
        """
        self.pipe.fit(data, labels)

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
        con_mat = confusion_matrix(labels, predictions)
        tn = con_mat[0][0]
        tp = con_mat[0][1]
        fp = con_mat[1][1]
        fn = con_mat[1][0]
        f1_score = tp / (tp + (.5*(fp + fn)))
        print(f'true positive: {tp} true negative: {tn} '
              f'false_positive: {fp} false negative: {fn} '
              f'f1 score: {f1_score}')

    def plot_confusion(self, data, labels):
        plot_confusion_matrix(self.pipe, data, labels, cmap=plt.cm.summer)
        plt.show()

    def grid_search(self, data, labels, n_iter=50, cv=3):
        """
        find best hyper-parameters
        """
        grid = RandomizedSearchCV(self.pipe, param_distributions=self.param_grid, n_iter=n_iter, cv=cv)
        grid.fit(data, labels)
        print(f'best params: {grid.best_params_} \n best score: {grid.best_score_}')

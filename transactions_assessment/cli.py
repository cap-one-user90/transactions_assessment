# _*_ coding: utf-8 _*_

"""Console script for transactions_assessment."""
from transactions_assessment.loaders.data_loaders import TransactionLoader, ModelDataLoader
from transactions_assessment.logging import logging_config
from transactions_assessment.detectors.detector_models import RFDetector
from logging.config import dictConfig
import click
import sys


dictConfig(logging_config)


@click.group()
def main(args=None):
    """console script for transactions_assessment."""
    return 0


@main.command()
@click.option('--datafile')
@click.option('--limit', default=None, type=int)
def train_model(datafile, limit):
    try:
        model_loader = ModelDataLoader(datafile, limit)
        x_train, x_test, y_train, y_test = model_loader.preprocess_data()
        detector = RFDetector()
        detector.set_samples(sampling_strategy='minority')
        detector.use_bootstrap(max_samples=.05)
        detector.pipe.set_params(**{'rf__n_estimators': 500, 'rf__min_samples_split': 2, 'rf__max_samples': 0.5,
                                    'rf__max_features': 'auto','rf__max_depth': 70})
        detector.train(x_train, y_train)
        detector.print_score(x_train, y_train, x_test, y_test)
        detector.print_confusion(x_test, y_test)

    except Exception as exc:
        click.secho(str(exc), err=True, fg='red')
    return


if __name__ == "__main__":
    sys.exit(main())

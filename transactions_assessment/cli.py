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
def load_data(datafile):
    try:
        loader = TransactionLoader(datafile)
        my_df = loader.load_unprocessed()
        print(f'total number of multi_swipes: {my_df["multi_swipe"].sum()}')
    except Exception as exc:
        click.secho(str(exc), err=True, fg='red')
    return


@main.command()
@click.option('--datafile')
@click.option('--limit', default=None, type=int)
def fit_model(datafile, limit):
    try:
        model_loader = ModelDataLoader(datafile, limit)
        x_train, x_test, y_train, y_test = model_loader.preprocess_data()
        detector = RFDetector()
        detector.set_samples(x_train, y_train)

    except Exception as exc:
        click.secho(str(exc), err=True, fg='red')
    return


if __name__ == "__main__":
    sys.exit(main())

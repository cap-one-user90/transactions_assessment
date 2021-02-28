# _*_ coding: utf-8 _*_

"""Console script for transactions_assessment."""
from transactions_assessment.loaders.data_loaders import TransactionLoader
from transactions_assessment.logging import logging_config
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
        my_df = loader.preprocess_data()
        print(f'total number of multi_swipes: {my_df["multi_swipe"].sum()}')
    except Exception as exc:
        click.secho(str(exc), err=True, fg='red')
    return


if __name__ == "__main__":
    sys.exit(main()) # pragma: no cover

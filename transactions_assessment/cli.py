# _*_ coding: utf-8 _*_

"""Console script for transactions_assessment."""
import sys
import click
from transactions_assessment.transactions_assessment import func1


@click.command()
def main(args=None):
    """console script for transactions_assessment."""
    click.echo("Hello, what would you like to search for?")
    return 0


if __name__ == "__main__":
    sys.exit(main()) # pragma: no cover

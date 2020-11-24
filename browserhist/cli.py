import logging

import click
import coloredlogs

from .browserhist import dump_browser_history, sync_browser_history

LOGGER_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s"
logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)
coloredlogs.install(fmt=LOGGER_FORMAT, level=logging.INFO, logger=LOGGER)


@click.group()
def cli():
    pass


@cli.command()
@click.option("-h", "--host", default="localhost", type=str)
@click.option("-p", "--port", default=9200, type=int)
@click.pass_context
def sync(ctx, host: str, port: str) -> None:
    """
    Fetches local browser data and uploads into elasticsearch
    """
    sync_browser_history(host, port)


@cli.command()
@click.option("-d", "--dest-dir", default="./", type=str)
@click.pass_context
def dump(ctx, dest_dir: str) -> None:
    """
    Dumps local browser data into local json files
    """
    dump_browser_history(dest_dir)

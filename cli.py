import click
import coloredlogs
import logging

from xps.browserhist.browserhist import sync_browser_history

LOGGER_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s"
logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)
coloredlogs.install(fmt=LOGGER_FORMAT, level=logging.INFO, logger=LOGGER)
print("-")

@click.group()
def cli():
    pass

@cli.command()
@click.pass_context
def sync(ctx):
    host = "xps"
    port = 9200
    sync_browser_history(host, port)

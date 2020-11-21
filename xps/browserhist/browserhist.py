import os
import sys
import glob
import logging
from elasticsearch import Elasticsearch
from dateutil.parser import parse
from urllib.parse import urlparse
from datetime import timedelta as td
from elasticsearch import helpers
import platform
from .browsers import Firefox, Chromium

LOGGER = logging.getLogger(__name__)


def _identify_platform():
    # it supports Linux, MacOS, and Windows platforms.
    # platform_table maps the name of user's OS to a platform code
    platform_table = {
        "linux": 0,
        "linux2": 0,
        "darwin": 1,
        "cygwin": 2,
        "win32": 2,
    }
    try:
        user_platformcode = platform_table[sys.platform]
        return user_platformcode
    except KeyError:

        class NotAvailableOS(Exception):
            pass

        raise NotAvailableOS("It does not support your OS.")


def fetch_linux_paths():
    browsers = [Firefox, Chromium]
    paths = []
    for browser in browsers:
        paths.extend(browser.fetch_linux_path())
    return paths


def get_database_paths():
    platform_code = _identify_platform()
    if platform_code == 0:
        return fetch_linux_paths()

def massage_es(row, browser_type, index, profile, node):
    url, title, ts = row
    ts_utc = parse(ts)
    ts = ts_utc - td(hours=5)
    hour = ts.hour
    weekday = ts.weekday()
    domain = urlparse(url).netloc.lstrip('www.')
    
    return {
        '_index': index,
        '_source': {
            'url': url,
            'title': title,
            'node': node,
            'timestamp': ts_utc,
            'hour': hour,
            'weekday': weekday,
            'domain': domain,
            'profile': profile,
            'browser': browser_type
        }
    }

def sync_to_es(history, browser_type, profile, node):
    es = Elasticsearch()
    browser_type = browser_type.lower()
    index = f"browser-{node}-{browser_type}-{profile}"
    actions = []
    LOGGER.info(f"Generating content for /{index}")
    for row in history:
        body = massage_es(row, browser_type, index, profile, node)
        actions.append(body)
    LOGGER.info(f"Committing to /{index}")
    es.indices.delete(index=index, ignore=[400, 404])
    helpers.bulk(es, actions, chunk_size=10000)

def sync_browser_history():
    node = platform.node()
    db_pahts = get_database_paths()
    for row in db_pahts:
        db, browser, profile = row
        LOGGER.info(f"Reading {db}")
        history = browser.read(db)
        sync_to_es(history, browser.__name__, profile, node)

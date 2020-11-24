import hashlib
import json
import logging
import os
import platform
from datetime import datetime as dt
from urllib.parse import urlparse

from dateutil import tz
from dateutil.parser import parse
from elasticsearch import Elasticsearch, helpers

from .browsers import Chromium, Firefox

LOGGER = logging.getLogger(__name__)


class OSResolutionFailure(Exception):
    pass


def _identify_platform() -> None:
    platform_table = {"Linux": 0, "Darwin": 1}
    try:
        user_platformcode = platform_table[platform.system()]
        return user_platformcode
    except KeyError:
        raise OSResolutionFailure("Unsupported operating system.")


def find_sqlite_tables() -> list:
    platform_code = _identify_platform()
    browsers = [Firefox, Chromium]
    paths = []
    for browser in browsers:
        if platform_code == 0:
            paths.extend(browser.fetch_linux_path())
        elif platform_code == 1:
            paths.extend(browser.fetch_macos_path())
    return paths


def massage_es(
    row: dict, browser_type: str, index: str, profile: str, node: str
) -> dict:
    data = massage_row(row, browser_type, profile, node)
    unique_str = data["url"] + str(data["timestamp"])
    hash_object = hashlib.md5(unique_str.encode()).hexdigest()
    data["timestamp"] = parse(data["timestamp"])
    data["local"]["timestamp"] = parse(data["local"]["timestamp"])
    return {"_index": index, "_id": hash_object, "_source": data}


def massage_row(row: str, browser_type: str, profile: str, node: str) -> dict:
    url, title, ts = row
    ts_local = parse(ts)
    ts_local = ts_local.replace(tzinfo=tz.tzlocal())
    ts_utc = ts_local.astimezone(tz.tzutc())
    domain = urlparse(url).netloc.lstrip("www.")

    return {
        "url": url,
        "title": title,
        "node": node,
        "timestamp": str(ts_utc),
        "domain": domain,
        "profile": profile,
        "browser": browser_type,
        "local": {
            "timestamp": str(ts_local),
            "hour": ts_local.hour,
            "weekday": ts_local.weekday(),
            "month": ts_local.strftime("%b"),
            "year": ts_local.year,
        },
    }


def sync_to_es(
    es: Elasticsearch, history: list, browser_type: str, profile: str, node: str
) -> None:
    browser_type = browser_type.lower()
    index = f"browser-{node}-{browser_type}-{profile}"
    actions = []
    LOGGER.info(f"Generating content for /{index}")
    for row in history:
        body = massage_es(row, browser_type, index, profile, node)
        actions.append(body)
    LOGGER.info(f"Committing to /{index}")
    # es.indices.delete(index=index, ignore=[400, 404])
    helpers.bulk(es, actions, chunk_size=10000)


def dump_to_file(
    dest_dir: str, history: list, browser_type: str, profile: str, node: str
) -> None:
    browser_type = browser_type.lower()
    basename = f"{node}-{browser_type}-{profile}.json"
    filepath = os.path.join(dest_dir, basename)
    if os.path.exists(filepath):
        LOGGER.warn(f"filepath {filepath} already exists. Deleting...")
        os.remove(filepath)

    LOGGER.info(f"Writing to file {filepath}")
    rows = [massage_row(row, browser_type, profile, node) for row in history]
    with open(filepath, "w") as w:
        json.dump(rows, w, indent=2)


def sync_browser_history(host: str, port: str, user="", pwd="") -> None:
    http_auth = (user, pwd) if pwd else None
    es = Elasticsearch([host], port=port, http_auth=http_auth)
    node = platform.node().lower()
    db_paths = find_sqlite_tables()
    for row in db_paths:
        db, browser, profile = row
        LOGGER.info(f"Reading {db}")
        history = browser.read(db)
        sync_to_es(es, history, browser.__name__, profile, node)


def dump_browser_history(dest_dir: str) -> None:
    node = platform.node().lower()
    db_paths = find_sqlite_tables()
    for row in db_paths:
        db, browser, profile = row
        LOGGER.info(f"Reading {db}")
        history = browser.read(db)
        dump_to_file(dest_dir, history, browser.__name__, profile, node)

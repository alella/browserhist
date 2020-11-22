import os
import glob
import shutil
import sqlite3
import logging
import tempfile

LOGGER = logging.getLogger(__name__)


class Browser:
    SQL = ""

    @classmethod
    def read(cls, db_path):
        tmpfile = tempfile.NamedTemporaryFile().name
        shutil.copy(db_path, tmpfile)
        query_result = []
        try:
            conn = sqlite3.connect(tmpfile)
            cursor = conn.cursor()
            cursor.execute(cls.SQL)
            query_result = cursor.fetchall()
        except Exception as e:
            LOGGER.error(f"Failed to process {cls.__name__}")
            LOGGER.exception(e)
        finally:
            os.remove(tmpfile)
        return query_result


class Firefox(Browser):
    SQL = """
    SELECT url, title, datetime((visit_date/1000000), 'unixepoch', 'localtime') AS visit_date 
    FROM moz_places INNER JOIN moz_historyvisits on moz_historyvisits.place_id = moz_places.id ORDER BY visit_date ASC
    """

    @classmethod
    def fetch_linux_path(cls):
        home = os.path.expanduser("~")
        paths = []  # (path, browser_class, profile)
        for path in glob.glob(
            os.path.join(home, ".mozilla", "firefox", "*", "places.sqlite")
        ):
            profile = path.split('/')[-2].lower().replace(' ', '')
            paths.append((path, cls, profile))
        return paths

    @classmethod
    def fetch_macos_path(cls):
        home = os.path.expanduser("~")
        paths = []  # (path, browser_class, profile)
        for path in glob.glob(
            os.path.join(home, "Library/Application Support/Firefox/Profiles", "*", "places.sqlite")
        ):
            profile = path.split('/')[-2].lower().replace(' ', '')
            paths.append((path, cls, profile))
        return paths

class Chromium(Browser):
    SQL = """
    SELECT urls.url, title, datetime((visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
    AS last_visit_time FROM urls INNER JOIN visits on urls.id=visits.url ORDER BY last_visit_time ASC
    """

    @classmethod
    def fetch_linux_path(cls):
        home = os.path.expanduser("~")
        paths = []  # (path, browser_class, profile)
        for path in glob.glob(os.path.join(home, ".config", "chromium", "*", "History")):
            profile = path.split('/')[-2].lower().replace(' ', '')
            paths.append((path, cls, profile))
        return paths

    @classmethod
    def fetch_macos_path(cls):
        home = os.path.expanduser("~")
        paths = []  # (path, browser_class, profile)
        for path in glob.glob(os.path.join(home, "Library/Application Support/Google/Chrome/", "*", "History")):
            profile = path.split('/')[-2].lower().replace(' ', '')
            paths.append((path, cls, profile))
        return paths

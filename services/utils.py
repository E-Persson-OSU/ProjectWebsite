from services.base_logger import logger
import services.govdeals as gd
import services.jailbase as jb
import services.db as db
import json
from pathlib import Path
from datetime import *

LASTRUN_PATH = Path("services/json-cache/") / "lastrun.json"

dateformat = "%m/%d/%Y, %H:%M:%S"


# wrap up both updates in one method, export current time to json after running, only run if json time past last 24hrs
def background_updates():
    data = {}
    try:
        with open(LASTRUN_PATH, "r") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        logger.info("%s: No information found in json file. First run.", e)
        data = None
    ctime = datetime.now()
    ltime = datetime.now()
    if data is not None:
        ltime = datetime.strptime(data["lastrun"], dateformat)
    else:
        update_govdeals()
        update_jailbase()
        with open(LASTRUN_PATH, "w") as f:
            data = {"lastrun": ctime.strftime(dateformat)}
            json.dump(obj=data, fp=f)
        logger.info("Background tasks completed. New data added to database.")
    # if it has been more than 24 hours, run background tasks, update json
    if ctime > ltime + timedelta(days=1):
        update_govdeals()
        update_jailbase()
        with open(LASTRUN_PATH, "w") as f:
            data = {"lastrun": ctime.strftime(dateformat)}
            json.dump(obj=data, fp=f)
        logger.info("Background tasks completed. New data added to database.")
    else:
        logger.info("Background tasks not run. Last run within 24hrs.")


# gather current listings, add to database
def update_govdeals():
    logger.info("Updating govdeals listings.")
    rows = gd.gather_listings()
    db.update_listings(rows)


def update_jailbase():
    ...

import logging
import services.govdeals as gd
import services.jailbase as jb
import services.db as db
import json
from pathlib import Path
from datetime import *

LASTRUN_PATH = Path("services/bin/") / "lastrun.json"
LOGGING_PATH = Path("services/logs/") / "utils.log"

dateformat = "%m/%d/%Y, %H:%M:%S"

# set up logging
logging.basicConfig(
    filename=LOGGING_PATH,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# wrap up both updates in one method, export current time to json after running, only run if json time past last 24hrs
def background_updates():
    data = {}
    try:
        with open(LASTRUN_PATH, "r") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        logging.error("%s: No information found in json file. First run.", e)
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
        logging.info("Background tasks completed. New data added to database.")
    # if it has been more than 24 hours, run background tasks, update json
    if ctime > ltime + timedelta(days=1):
        update_govdeals()
        update_jailbase()
        with open(LASTRUN_PATH, "w") as f:
            data = {"lastrun": ctime.strftime(dateformat)}
            json.dump(obj=data, fp=f)
        logging.info("Background tasks completed. New data added to database.")
    else:
        logging.info("Background tasks not run. Last run within 24hrs.")


# gather current listings, add to database
def update_govdeals():
    ...


def update_jailbase():
    ...

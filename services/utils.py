# background tasks for worker to run
import services.govdeals as gd
import services.jailbase as jb
import services.db as db
import json
from pathlib import Path
from datetime import *

lastrun_path = Path("services/bin/") / "lastrun.json"

dateformat = "%m/%d/%Y, %H:%M:%S"


# wrap up both updates in one method, export current time to json after running, only run if json time past last 24hrs
def background_updates():
    data = {}
    try:
        with open(lastrun_path, "r") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print("{}\nNo information found in json file. First run.".format(e))
        data = None
    ctime = datetime.now()
    ltime = datetime.now()
    if data is not None:
        ltime = datetime.strptime(data["lastrun"], dateformat)
    else:
        update_govdeals()
        update_jailbase()
        with open(lastrun_path, "w") as f:
            data = {"lastrun": ctime.strftime(dateformat)}
            json.dump(obj=data, fp=f)
    # if it has been more than 24 hours, run background tasks, update json
    if ctime > ltime + timedelta(days=1):
        update_govdeals()
        update_jailbase()
        with open(lastrun_path, "w") as f:
            data = {"lastrun": ctime.strftime(dateformat)}
            json.dump(obj=data, fp=f)
    else:
        print("Run in last 24hrs.")


# gather current listings, add to database
def update_govdeals():
    ...


def update_jailbase():
    ...

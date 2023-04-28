import logging
from pathlib import Path
import os

LOGGING_PATH = Path("services/logs/") / "weblogs.log"
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

if not LOGGING_PATH.parent.exists():
    os.makedirs(LOGGING_PATH.parent)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# create a file handler
file_handler = logging.FileHandler(LOGGING_PATH)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(FORMAT))

# add the handlers to the logger
logger.addHandler(file_handler)

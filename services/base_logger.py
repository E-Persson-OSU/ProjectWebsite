import logging
from pathlib import Path

LOGGING_PATH = Path("services/logs/") / "weblogs.log"
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    filename=LOGGING_PATH,
    filemode="w",
    format=FORMAT,
    level=logging.ERROR,
)

logger = logging

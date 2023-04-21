import os
import redis
from pathlib import Path
from rq import Worker, Queue, Connection
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import sys

LOGGING_PATH = Path("services/logs/") / "worker.log"

logging.basicConfig(
    filename=LOGGING_PATH,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

listen = ["high", "default", "low"]

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

conn = redis.from_url(redis_url)


if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

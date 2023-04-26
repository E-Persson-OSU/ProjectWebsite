import os
import redis
from pathlib import Path
from rq import Worker, Queue, Connection

from services.base_logger import logger
import sys

listen = ["high", "default", "low"]

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

conn = redis.from_url(redis_url)


if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

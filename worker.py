import os
import redis
from rq import Worker, Queue, Connection
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

listen = ["high", "default", "low"]

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

conn = redis.from_url(redis_url)


if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

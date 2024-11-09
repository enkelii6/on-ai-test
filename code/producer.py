import redis.asyncio as redis
from rq import Queue


class Producer:
    _instance = None

    def __new__(cls, redis_conn: redis.Redis = None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.queue = Queue(connection=redis_conn)
        return cls._instance

    def __init__(self, redis_url: str = None):
        pass

    def enqueue_job(self, func, *args, **kwargs):
        return self.queue.enqueue(func, *args, **kwargs)

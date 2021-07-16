# --------------------------------------------------------------------------
# worker process to listen for queued tasks
# listened for a queue called default and established a connection to the
# Redis server on localhost:6784 6379
# --------------------------------------------------------------------------
import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

# redis_url = os.getenv('REDIS_URL')
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# redis_url = os.getenv('REDISTOGO_URL', 'redis://redis.dna.local:6379')
# redis_url = os.getenv('REDISTOGO_URL', 'redis://redis-dev.dna.local:6379')
timeout = 7200

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
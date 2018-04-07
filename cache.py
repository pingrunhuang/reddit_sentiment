import os

class cache_redis:
    client = None
    host = "localhost"
    port = 6379
    redis_db = 0
    
    def __init__(self):
        self.client = Redis(host=self.host, port=self.port, db=self.redis_db)
    
    def get(self, key):
        return self.client.get(key)
    
    def set(self, key, value, expire_seconds=10):
        return self.client.set(name=key, value=value, ex=expire_seconds, nx=True)

# the cache for exporting
cache = None
from redis import Redis
cache=cache_redis()


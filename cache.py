from redis import Redis

host = "localhost"
port = 6379
redis_db = 0

class cache_redis():
    
    def __init__(self):
        self.client = Redis(host=host, port=port, db=redis_db)
    
    def get(key):
        return self.client.get(key)
    
    def set(key, value, expire_seconds=10):
        return self.client.set(name=key, value=value, ex=expire_seconds, nx=True)


cache=cache_redis()

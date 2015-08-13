# -*- coding:utf-8 -*-


# Third-Party imports
import redis

# Project imports


class RedisBackend(object):
    """Redis task result store."""

    def __init__(self, server):
        self.redis = redis.Redis(**server)

    def send(self, key, value):
        self.redis.rpush(key, value)

    def accept(self, key):
        return self.redis.lpop(key)

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        return self.redis.delete(key)

# -*- coding:utf-8 -*-

#StdLib imports
import logging

#Third-Party imports
import redis

#Project imports
from django.conf import REDIS_CONF


class RedisBackend(object):
    """Redis task result store."""

    def __init__(self):
        self.redis = redis.Redis(**REDIS_CONF)

    def send(self, key, value):
        #logging
        self.redis.rpush(key, value)

    def accept(self, key):
        return self.redis.lpop(key)

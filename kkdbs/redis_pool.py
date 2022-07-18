# -*- coding: utf-8 -*-
# @Author: vekair

import redis


class RedisPool(object):
    def __init__(self, REDIS_HOST, REDIS_PORT, REDIS_PASS):
        self.host = REDIS_HOST
        self.port = REDIS_PORT
        self.pass_word = REDIS_PASS

    def build_redis(self, redis_db=0):
        """建立链接"""
        rdp = redis.ConnectionPool(host=self.host, port=self.port, db=redis_db, password=self.pass_word)
        return redis.StrictRedis(connection_pool=rdp)

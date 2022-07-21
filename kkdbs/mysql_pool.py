# -*- coding: utf-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlConnectionPool():
    __pool = None

    def __init__(self,
                 host, db, user, password, port=None,
                 mix_cached=None, max_cached=None, max_shared=None, max_connections=None,
                 max_usage=None,
                 ):
        self.MYSQL_DB_HOST = host
        self.db = db
        self.MYSQL_DB_USER = user
        self.MYSQL_DB_PWD = password
        self.MYSQL_PORT = 3306 if port is None else port
        self.DB_MIN_CACHED = 5 if mix_cached is None else mix_cached
        self.DB_MAX_CACHED = 10 if max_cached is None else max_cached
        self.DB_MAX_SHARED = 30 if max_shared is None else max_shared
        self.DB_MAX_CONNECTIONS = 50 if max_connections is None else max_connections
        self.DB_MAX_USAGE = 0 if max_usage is None else max_usage

        """
        DB_MIN_CACHED:最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
        DB_MAX_CACHED:最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
        DB_MAX_SHARED:当连接数达到这个数，新请求的连接会分享已经分配出去的连接
        DB_MAX_CONNECTIONS:最大的连接数
        maxusage: 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
        DB_MAX_USAGE: 
        """

    # 创建数据库连接conn和游标cursor
    def __enter__(self):
        self.conn = self.__getconn()
        self.cursor = self.conn.cursor()

    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=pymysql,
                mincached=self.DB_MIN_CACHED,
                maxcached=self.DB_MAX_CACHED,
                maxshared=self.DB_MAX_SHARED,
                maxconnections=self.DB_MAX_CONNECTIONS,
                blocking=True,
                maxusage=self.DB_MAX_USAGE,
                host=self.MYSQL_DB_HOST,
                user=self.MYSQL_DB_USER,
                passwd=self.MYSQL_DB_PWD,
                db=self.db,
                port=self.MYSQL_PORT,
                cursorclass=pymysql.cursors.DictCursor
            )

        return self.__pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        if self.__pool:
            self.__pool.close()

    # 关闭连接归还给链接池
    def _close(self):
        self.cursor.close()
        self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn

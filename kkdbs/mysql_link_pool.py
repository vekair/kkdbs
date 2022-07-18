# -*- coding: utf-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlConnectionPool():
    __pool = None

    def __init__(self,
                 db, DB_MIN_CACHED=None, DB_MAX_CACHED=None, DB_MAX_SHARED=None, DB_MAX_CONNECTIONS=None,
                 DB_MAX_USAGE=None, MYSQL_DB_HOST=None, MYSQL_DB_USER=None, MYSQL_DB_PWD=None, MYSQL_PORT=None,
                 ):
        self.db = db
        self.DB_MIN_CACHED = 5 if DB_MIN_CACHED is None else DB_MIN_CACHED
        self.DB_MAX_CACHED = 10 if DB_MAX_CACHED is None else DB_MAX_CACHED
        self.DB_MAX_SHARED = 30 if DB_MAX_SHARED is None else DB_MAX_SHARED
        self.DB_MAX_CONNECTIONS = 50 if DB_MAX_CONNECTIONS is None else DB_MAX_CONNECTIONS
        self.DB_MAX_USAGE = 0 if DB_MAX_USAGE is None else DB_MAX_USAGE
        self.MYSQL_DB_HOST = MYSQL_DB_HOST
        self.MYSQL_DB_USER = MYSQL_DB_USER
        self.MYSQL_DB_PWD = MYSQL_DB_PWD
        self.MYSQL_PORT = 3306 if MYSQL_PORT is None else MYSQL_PORT

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
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn

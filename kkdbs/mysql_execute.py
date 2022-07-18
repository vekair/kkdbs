# -*- coding: utf-8 -*-
# @Author: vekair

import logging
from mysql_pool import MysqlConnectionPool
log = logging.Logger(__name__)

class MysqlExecute():
    def __init__(self, db):
        self.db = MysqlConnectionPool(db)

    # 封装执行命令
    def execute(self, sql, param=None, autoclose=False):
        """
        【主要判断是否有参数和是否执行完就释放连接】
        :param sql: 字符串类型，sql语句
        :param param: sql语句中要替换的参数"select %s from tab where id=%s" 其中的%s就是参数
        :param autoclose: 是否关闭连接
        :return: 返回连接conn和游标cursor
        """
        cursor, conn = self.db.getconn()  # 从连接池获取连接

        count = 0
        try:
            # count : 为改变的数据条数
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            log.warn(e)
        return cursor, conn, count

    def close(self, cursor, conn):
        """释放连接归还给连接池"""
        cursor.close()
        conn.close()

    # 增加
    def insertone(self, sql, param):
        conn = cursor = None
        try:
            cursor, conn, count = self.execute(sql, param)
            _id = cursor.lastrowid  # 获取当前插入数据的主键id，该id应该为自动生成为好
            conn.commit()
            self.close(cursor, conn)
            # return count
            # 防止表中没有id返回0
            if _id == None or _id == 0:
                return True
            return _id
        except Exception as e:
            log.warn(e)
            if conn:
                conn.rollback()
                self.close(cursor, conn)

    # 查询所有
    def selectall(self, sql, param=None):
        cursor = conn = None
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchall()
            return res
        except Exception as e:
            log.warn(e)
            if conn:
                self.close(cursor, conn)

    # 查询单条
    def selectone(self, sql, param=None):
        cursor = conn = None
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            log.warn("error_msg:", e.args)
            if conn:
                self.close(cursor, conn)

    # 更新
    def update(self, sql, param=None):
        conn = cursor = None
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            log.warn(e)
            if conn:
                conn.rollback()
                self.close(cursor, conn)

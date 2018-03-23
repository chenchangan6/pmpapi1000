#!flask/bin/python3
# -*- coding: utf-8 -*-
import pymongo
import traceback
from config1000.configs import MONGODB_CONFIG


class Singleton(object):
    # 单例模式写法,参考：http://ghostfromheaven.iteye.com/blog/1562618
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


# 这个是一个通用方法，请忽略命名使用大写字母的下划线提示。
def on_error(eor):
    return eor


class MongoConn(Singleton):
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
            self.username = MONGODB_CONFIG['username']
            self.password = MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception as e:
            eor = str(traceback.format_exc(e))
            on_error(eor)


def check_connected(conn):
    # 检查是否连接成功
    if not conn.connected:
        raise ValueError(f'stat:connected Error')


def save(table, value):
    # 一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].save(value)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def insert(table, value):
    # 可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].insert(value, continue_on_error=True)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def update(table, conditions, value, s_upsert=False, s_multi=False):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def upsert_mary(table, datas):
    # 批量更新插入，根据‘_id’更新或插入多条记录。
    # 把'_id'值不存在的记录，插入数据库。'_id'值存在，则更新记录。
    # 如果更新的字段在mongo中不存在，则直接新增一个字段
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        bulk = my_conn.db[table].initialize_ordered_bulk_op()
        for data in datas:
            _id = data['_id']
            bulk.find({'_id': _id}).upsert().update({'$set': data})
        bulk.execute()
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def upsert_one(table, data):
    # 更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'_id': data.get}
        if not my_conn.db[table].find_one(query):
            my_conn.db[table].insert(data)
        else:
            data.pop('_id')  # ɾ��'_id'��
            my_conn.db[table].update(query, {'$set': data})
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def find_one(table, value):
    # 根据条件进行查询，返回一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].find_one(value)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def find(table, value):
    # 根据条件进行查询，返回所有记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].find(value)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def select_colum(table, value, colum):
    # 查询指定列的所有值
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].find(value, {colum: 1})
    except Exception as e:
        on_error(str(traceback.format_exc(e)))

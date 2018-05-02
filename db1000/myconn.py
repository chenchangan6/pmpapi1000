#!flask/bin/python3.6
# -*- coding: utf-8 -*-
# -*- author: Charles Chen
import pymongo
import traceback
from config1000.configs import MONGODB_CONFIG


# 本方法中，为了使用方便进行了去ID改造，
# 即从MONGODB返回的数据没有带ID这个字段（因为ID字段是OBJECT类型，需要单独处理，而且本例中基本上用不到ID）
# 去掉的方法是，在 FIND({},{"_id":0})).
# 凡是这样的写法的都是已经去掉自动返回ID的。

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


# def upsert_one(table, data):
#     # 更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
#     try:
#         my_conn = MongoConn()
#         check_connected(my_conn)
#         query = {'_id': data.get}
#         if not my_conn.db[table].find_one(query):
#             my_conn.db[table].insert(data)
#         else:
#             data.pop('_id')  # 删除'_id'键
#             my_conn.db[table].update(query, {'$set': data})
#     except Exception as e:
#         on_error(str(traceback.format_exc(e)))

def upsert_one(table, query, data):
    # query为查询条件，如：query={'_id': data.get},注：query必须为一个JSON
    # 更新插入一条数据，例如:根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].update_one(query, {'$set': data}, upsert=True)
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


def find_desc(table, field):
    # 根据条件进行查询，返回所有记录（已经去掉id）并（倒序），此方法为 find方法的扩展.sort用法。
    # table 传集合的名称，field 传 倒序字段的名称。
    # 例如：userlist = find_desc("users", "_id")，返回一个倒序的Josn集合（注意：包含ID为Object类型）
    # 返回对象使用时需要:
    # user_list = []
    # userlist = find_desc("users", "_id")
    # for x in userlist:
    #     x.pop("_id")
    #     user_list.append(x)
    # return user_list
    try:

        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].find({}, {'_id': 0}).sort(field, pymongo.DESCENDING)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def select_colum(table, value, *colum):
    # 查询指定列的所有值（已经去掉id），table为集合名称，value是查询条件，*colum为想显示的列的名称,*colum可以为多个列名，
    # 例如：
    # selct_colum("users", {'username': args['username']}, 'username')
    # 相当于给数据库发送指令 db.users.find({username:'cca'},{username:1})
    # { "_id" : ObjectId("5ab4fedbbad7311d33686ec5"), "username" : "cca" }
    # { "_id" : ObjectId("5ab5043df8001641e5be1cde"), "username" : "cca" }
    # 如果需要查询用户名和密码,添加为username:cca，显示username和pwd两列。
    # selct_colum("users", {'username': args['username']}, 'username','pwd')
    # 相当于给数据库发送指令 db.users.find({username:'cca'},{username:1,pwd:1})
    # 返回结果过为：
    # { "_id" : ObjectId("5ab4fedbbad7311d33686ec5"), "username" : "cca","pwd":"123" }
    # { "_id" : ObjectId("5ab5043df8001641e5be1cde"), "username" : "cca","pwd":"123" }
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        showfileds = {}
        for filed in colum[0]:
            showfileds[filed] = 1
        showfileds['_id'] = 0

        return my_conn.db[table].find(value, showfileds)
        # return my_conn.db[table].find(value, {colum[0][0]: 1, '_id': 0})
    except Exception as e:
        on_error(str(traceback.format_exc(e)))


def delete_many(table, value):
    # 删除指定条件的所有的条目
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].delete_many(value)
    except Exception as e:
        on_error(str(traceback.format_exc(e)))

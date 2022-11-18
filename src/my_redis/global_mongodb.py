import pymongo
from src.config import conf


def _init():
    global _global_mongodb
    mongoDbUrl = 'mongodb://' + \
        conf.get('mongodb', 'url') + ':' + conf.get('mongodb', 'port') + '/'
    client = pymongo.MongoClient(mongoDbUrl)
    _global_mongodb = client['xunhuan']


def insert_one(table, dict):
    res = _global_mongodb[table].insert_one(dict)
    return res.inserted_id


def insert_many(table, dic):
    res = _global_mongodb[table].insert_many(dic)
    return res


def find_one(table):
    res = _global_mongodb[table].find_one()
    return res


def find(table):
    res = _global_mongodb[table].fine()
    return res

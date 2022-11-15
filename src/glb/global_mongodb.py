import pymongo
from src.config import global_config


def _init():
    global _global_mongodb
    mongoDbUrl = 'mongodb://' + global_config.get_value('mongodb.url') + ':' + global_config.get_value('mongodb.port') + '/'
    client = pymongo.MongoClient(mongoDbUrl)
    _global_mongodb = client['xunhuan']

def insert_one(table,dict):
    res = _global_mongodb[table].insert_one(dict)
    return res.inserted_id

def insert_many(table,dic):
    res = _global_mongodb[table].insert_many(dic)
    return res

def find_one(table):
    res = _global_mongodb[table].find_one()
    return res

def find(table):
    res = _global_mongodb[table].fine()
    return res
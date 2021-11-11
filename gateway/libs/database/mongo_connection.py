from typing import AnyStr

from pymongo import MongoClient
from pymongo.collection import Collection

from gateway.config import MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD


def get_mongo_connection(database: AnyStr, collection: AnyStr) -> Collection:
    connection = {
        'host': MONGO_HOST,
        'port': int(MONGO_PORT),
        'username': MONGO_USER,
        'password': MONGO_PASSWORD,
        'authSource': 'admin',
        'authMechanism': 'SCRAM-SHA-1'
    }
    return MongoClient(**connection)[database][collection]

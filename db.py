from pymongo import MongoClient


def get_db():
    client = MongoClient('localhost', 27017)

    return client.db_vaccine
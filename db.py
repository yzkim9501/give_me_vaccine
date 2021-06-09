from pymongo import MongoClient


def get_db():
    # client = MongoClient('15.164.169.31', 27017, username="test", password="test")
    client = MongoClient('localhost', 27017)
    return client.db_vaccine
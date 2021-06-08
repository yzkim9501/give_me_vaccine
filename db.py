from pymongo import MongoClient


def get_db():
    client = MongoClient('15.164.169.31', 27017, username="test", password="test")

    return client.db_vaccine
from pymongo import MongoClient
import json


MONGO_HOST = 'mongodb://localhost/israeli_tweets'

"""
Set a Mongodb with this details:
MONGO_HOST = 'mongodb://localhost/israeli_tweets'
NAME OF DB - israeli_tweets
NAME OF COLLECTION - tweets
"""

class DBClient():
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self, db_path=MONGO_HOST):
        try:
            self.client = MongoClient(db_path)
        except Exception as e:
            print(e)

    def set_tweets_db(self):
        self.db = self.client.israeli_tweets

    def set_tweets_collection(self):
        self.collection = self.db.tweets

    def close(self):
        try:
            self.client.close()
            print("client closed.")
        except Exception as e:
            print(e)

    def insert_document(self, data):
        data_json_format = json.loads(data)
        try:
            self.collection.insert_one(data_json_format)
        except Exception as e:
            print(e)


"""
===  Example for using this module:  ====
if __name__ == '__main__':
    data = '{"value": 1 }'
    db_client = DBClient()
    db_client.connect()
    db_client.set_tweets_db()
    db_client.set_tweets_collection()
    db_client.insert_document(data)
    db_client.close()
"""
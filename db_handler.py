from pymongo import MongoClient
import json


MONGO_HOST = 'mongodb://localhost/israeli_tweets'

"""
Set a Mongodb with this details:
MONGO_HOST = 'mongodb://localhost/israeli_tweets'
NAME OF DB - israeli_tweets
NAME OF COLLECTION - tweets
"""


# Search types
SINGLE_SEARCH = "single_search"
UNI_SEARCH = "uni_search"
INTER_SEARCH = "inter_search"


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
        except Exception as e:
            print(e)

    def insert_document(self, document):
        document_json_format = json.loads(document)
        try:
            self.collection.insert_one(document_json_format)
        except Exception as e:
            print(e)

    def find_single_document(self, param):
        if not param:
            return None
        document = None
        try:
            document = self.collection.find_one(param)
        except Exception as e:
            print(e)
        return document

    def find_documents(self, param):
        if not param:
            return None
        documents = None
        try:
            documents = list(self.collection.find(param))
        except Exception as e:
            print(e)
        return documents

"""
    ====    REDUNDANT CODE     ====
    
    def find_documents_unification(self, param_list):
        if not param_list:
            return None
        documents_list = []
        try:
            db_documents = list(self.collection.find())     # convert to list
            for doc in db_documents:
                i = 0
                while i < len(param_list):
                    if str(param_list[i]) in str(doc):    # 1 parameter is enough to enter document_list
                        documents_list.append(doc)
                        break
                    i = i + 1
        except Exception as e:
            print(e)
        return documents_list

    def find_documents_intersection(self, param_list):
        if not param_list:
            return None
        documents_list = []
        try:
            db_documents = list(self.collection.find())    # convert to list
            documents_list = db_documents.copy()           #init document_list to have all docs.
            for doc in db_documents:
                i = 0
                while i < len(param_list):
                    if str(param_list[i]) not in str(doc):    # 1 parameter not included is enough to be removed!
                        documents_list.remove(doc)
                        break
                    i = i + 1
        except Exception as e:
            print(e)
        return documents_list
"""

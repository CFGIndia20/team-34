from __future__ import division
from db_connectivity import *
import pymongo

'''
The OhlcRepo performs all database operations on a given collection.
'''


class OhlcRepo(object):

    db_inst = None
    db_cli = None

    def __init__(self):
        mongo = MongoCon()
        self.db_cli = mongo.get_connection()

    def drop_collection(self, collection_name):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.drop()

    def insert_record(self, collection_name, query, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.update_one(query, insert_doc, upsert=True)

    def insert_record_one(self, collection_name, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.insert_one(insert_doc)

    def insert_many_records(self, collection_name, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        return self.db_inst.insert_many(insert_doc)

    def find_records(self, collection_name):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find())

    def find_records_with_query(self, collection_name, query):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query))

    def find_records_with_limit(self, collection_name, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find().sort('timestamp', pymongo.DESCENDING).limit(limit))

    def find_record_with_limit(self, collection_name, query, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).limit(limit))

    def find_records_with_sort(self, collection_name, query):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).sort('timestamp', pymongo.DESCENDING))

    def find_records_with_sort_field(self, collection_name, query, field):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).sort(field, pymongo.DESCENDING))

    def find_record_with_projection_limit(self, collection_name, query, projection, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection).sort('timestamp', pymongo.DESCENDING).limit(limit))

    def find_record_with_projection(self, collection_name, query, projection):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection))

    def find_record_with_projection_sort(self, collection_name, query, projection):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection).sort('timestamp', pymongo.DESCENDING))

    def find_record_with_sort_limit(self, collection_name, query, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query).sort('timestamp', pymongo.ASCENDING).limit(limit))

    def find_record_with_sort_limit_projection(self, collection_name, query, projection, limit):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.find(query, projection).sort('timestamp', pymongo.ASCENDING).limit(limit))

    def aggregate_with_projection_sort(self, collection_name, pipeline):
        self.db_inst = self.db_cli[collection_name]
        return list(self.db_inst.aggregate(pipeline))

    def update_query(self, collection_name, query_doc, insert_doc):
        self.db_inst = self.db_cli[collection_name]
        self.db_inst.update_one(query_doc, {'$set': insert_doc})
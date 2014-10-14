__author__ = 'Tamir'

import bson
import json
import pymongo
import re

TEST_COLLECTION = "c2q_test.txt"
DB_COLLECTION = "test_collection.json"
IN_DB = "<--in_db-->"
CHANGED_CODE = re.compile('<--[0-9]+-->')
NOT_IN_DB = "<--not_in_db-->"

txt_file = open(TEST_COLLECTION, 'r')
i = 0
for query in txt_file.read().split("<--NEW CODE-->"):
    if len(query) > 0:
        if IN_DB==query.split('\n')[1]:
            print "in DB"
        elif CHANGED_CODE.match(query.split('\n')[1]):
            print "changed"
        elif NOT_IN_DB==query.split('\n')[1]:
            print "not in DB"
        #else:


#if __name__ == '__main__':
client = pymongo.MongoClient()
db = client.dataset
documents = db.all_queries
queries = db.test_queries
i=0
for doc in documents.find():
    if i==1:
        print doc
    i+=1
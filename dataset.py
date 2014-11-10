__author__ = 'Tamir'

from random import randint
import pymongo
import re

TEST_COLLECTION = "c2q_test.txt"
DB_COLLECTION = "test_collection.json"
IN_DB = "<--in_db-->"
CHANGED_CODE = re.compile('<--[0-9]+-->')
NOT_IN_DB = "<--not_in_db-->"


def set_in_db():
    used = []
    count = 0
    for count in range(0, 25):
        codeID = randint(0, 999)
        while codeID in used:
            codeID = randint(0, 999)
        used.append(codeID)
        print count
        # queries.insert({"code_id": count, "code": documents.find({'code_id': str(codeID)})[0]['code'], "type": "in_db"})
        count += 1
    return count


if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client.dataset
    documents = db.all_queries
    queries = db.test_queries

    txt_file = open(TEST_COLLECTION, 'r')
    count = set_in_db()

    print "bla"

    for query in txt_file.read().split("<--NEW CODE-->"):
        if len(query) > 0:
            if CHANGED_CODE.match(query.split('\n')[1]):
                print count
                # queries.insert({"code_id": count, "code": query.split(query.split('\n')[1])[1], "type": "changed"})
            elif NOT_IN_DB == query.split('\n')[1]:
                print count
                # queries.insert({"code_id": count, "code": query.split(query.split('\n')[1])[1], "type": "not_in_db"})
            else:
                break
            count += 1
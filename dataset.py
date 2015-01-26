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
    """
    This function choose randomly 25 different queries from the collection documents and insert them to the collection queries
    :return: the number of queries inserted to the collection
    """
    used = []
    count_queries = 0
    for count_queries in range(0, 25):
        code_id = randint(0, 999)
        while code_id in used:
            code_id = randint(0, 999)
        used.append(code_id)
        queries.insert(
            {"code_id": count, "code": documents.find({'code_id': str(code_id)})[0]['code'], "type": "in_db"})
        count_queries += 1
    return count_queries


def set_txt_file(count_queries):
    """
    This function parse the text file TEST_COLLECTION, and insert each code with his relevant data to the collection queries
    :param count_queries: the number of queries already in the collection
    """
    for query in txt_file.read().split("<--NEW CODE-->"):
        if len(query) > 0:
            if CHANGED_CODE.match(query.split('\n')[1]):
                changed_keys.append(query.split('\n')[1].split('-')[2])
                queries.insert({"code_id": count, "code": query.split(query.split('\n')[1])[1], "type": "changed"})
            elif NOT_IN_DB == query.split('\n')[1]:
                print "bla"
                queries.insert({"code_id": count, "code": query.split(query.split('\n')[1])[1], "type": "not_in_db"})
            else:
                break
            count_queries += 1


if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client.dataset
    documents = db.all_queries
    queries = db.test_queries

    changed_keys = []

    txt_file = open(TEST_COLLECTION, 'r')
    count = set_in_db()
    set_txt_file(count)


    # gets the ID of each code in queries which is also in documents or is in documents and was edited
    changed_list = []
    for a in documents.find():
        if a['question_id'] in changed_keys:
            changed_list.append(a['code_id'])

    in_db_codes = []
    for a in queries.find():
        if a['type'] == "in_db":
            in_db_codes.append(a['code'])

    in_db_code_id = []
    for a in documents.find():
        if a['code'] in in_db_codes:
            in_db_code_id.append(a['code_id'])

    print changed_list
    print in_db_code_id
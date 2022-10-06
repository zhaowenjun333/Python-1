import csv
import pymongo

mongo_client = pymongo.MongoClient()

with open('./movie_world.csv', 'r', encoding='utf-8-sig') as f:
    data = csv.DictReader(f)
    for row in data:
        print(dict(row))
        mongo_client['crawl_one']['collection_two'].insert_one(dict(row))


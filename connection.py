import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017")
my_db = my_client['sentiment']
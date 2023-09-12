from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoOp:

    def __init__(self):
        self.uri = "mongodb+srv://moonman369:ayan%23123@cluster0.gblpsp7.mongodb.net/?retryWrites=true&w=majority"
        self.db = None
        self.collection = None
    
    def connect(self, db_name):
        client = MongoClient(self.uri)
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.db = client.get_database(db_name)
            return self.db
        except Exception as e:
            print(e)

    def get_collection(self, collection_name):
        try:
            self.collection = self.db[collection_name]
            print(f"Found collection: {collection_name}")
            return self.collection
        except Exception as e:
            print(e)

    def insert(self, insert_dict):
        try:
            self.collection.insert_one(insert_dict)
            print("Insert successful -->",insert_dict)
        except Exception as e:
            print(e)

    def find(self, short):
        try:
            res = self.collection.find_one(short)
            print(f"Result for \"{short}\":", res)
            return res["url"] if res else None
        except Exception as e:
            print(e)

    def delete_all(self):
        try:
            self.collection.delete_many({})
            print("Deleted all documents from collection.")
        except Exception as e:
            print(e)



# mongo = MongoOp()
# mongo.connect("shortify")
# mongo.get_collection("urlList")

# # mongo.insert({"short":"lsn", "url":"https://lensin-beta.netlify.com"})
# mongo.delete_all()
# print(mongo.find({"short":"hi"}))
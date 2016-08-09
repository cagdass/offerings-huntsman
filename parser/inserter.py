from pymongo import MongoClient

class Inserter:
    def __init__(self, host = 'localhost', port = 27017, collectionName = '20161', cleanInit = True):
        self.host = host
        self.port = port
        self.collectionName = collectionName
        self.cleanInit = cleanInit
        client = MongoClient(host, port)
        db = client.offerings # Change the database name
        collection = db['semester' + collectionName]
        if cleanInit:
            collection.delete_many({})
        self.collection = collection

    def getCollection(self):
        return self.collection

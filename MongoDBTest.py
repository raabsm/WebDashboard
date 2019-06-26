import pymongo

from bson import ObjectId

connection = pymongo.MongoClient('localhost', 27017)

database = connection['mydb_01']

collection = database['mycol_01']

data = {'Name': "Sam"}

document = collection.insert_one(data)

print(document.inserted_id)

updatedData = {'Name': 'David'}
collection.update_one({'_id':ObjectId(str(document.inserted_id))}, {"$set": updatedData}, upsert=True)

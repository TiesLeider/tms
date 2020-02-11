import pymongo
c = pymongo.MongoClient("localhost:27017")

col = c["tms"]["tram_storingen"]
col.delete_many({})

c["tms"]["tram_storing_data"].drop()


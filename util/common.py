from wikipedia_scraper import settings
import pymongo

def load_from_mongo():
    connection = pymongo.MongoClient(
        settings.MONGODB_SERVER,
        settings.MONGODB_PORT
    )
    db = connection[settings.MONGODB_DB]
    collection = db[settings.MONGODB_COLLECTION]
    return [x for x in collection.find()]

import os
from pymongo import MongoClient
from .GetReviews import get_reviews
from .mongo_client import get_mongo_client

load_dotenv()

client= MongoClient(
	f"mongodb://{os.getenv('MONGO_ROOT_USER')}:{os.getenv('MONGO_ROOT_PASSWORD')}" 
 	f"@{os.getenv('MONGO_HOST', 'localhost')}:27017/"
 	f"{os.getenv('DB_NAME', 'moviesdb')}

db = client[os.getenv("DB_NAME", "moviesdb")]
reviews_collection = db.reviews



def insert_reviews():
    '''Insert movie and their corresponding emotion 
       into a MongoDB collection'''
    for review in get_reviews():
    	reviews_collection.insert_one(review)
    client.close()
    



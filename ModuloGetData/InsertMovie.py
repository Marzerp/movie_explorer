import os
from pymongo import MongoClient
from .GetReviews import get_reviews
from .mongo_client import get_mongo_client

load_dotenv()

client= MongoClient(
	f"mongodb://{os.getenv('MONGO_ROOT_USER')}:{os.getenv('MONGO_ROOT_PASSWORD')}" 
 	f"@{os.getenv('MONGO_HOST', 'localhost')}:27017/"
 	f"{os.getenv('MONGO_APP_DB', 'moviesdb')}

db = client[os.getenv("MONGO_APP_DB", "moviesdb")]
reviews_collection = db.reviews



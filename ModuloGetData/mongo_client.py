from pymongo import MongoClient
import os

print("*** Inicio mongo-client ***")

load_dotenv()

def get_mongo_client():
    username = os.getenv("MONGO_ROOT_USER")
    password = os.getenv("MONGO_ROOT_PASSWORD")
    db_name = os.getenv("MONGO_APP_DB")
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT", "27017")

    client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{db_name}")
    return client[db_name]
print("*** FIN mongo-client ***")


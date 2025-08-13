from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()


def connect_Db():
    mongodb_uri = os.getenv("MONGODB_CONNECTION_STRING")
    
    if not mongodb_uri:
        mongodb_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URL")
    
    if not mongodb_uri:
        raise ValueError("MongoDB connection string not found. Please set MONGODB_CONNECTION_STRING, MONGODB_URI, or MONGO_URL environment variable.")
    
    client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
                          
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e
    
    return client['mydatabase']


db = connect_Db()
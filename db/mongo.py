import os

from pymongo import MongoClient
from pymongo.database import Database


def get_database():
    cluster_name = os.environ.get('MONGO_CLUSTER_NAME')
    cluster_password = os.environ.get('MONGO_CLUSTER_PASSWORD')
    cluster_server = os.environ.get('MONGO_CLUSTER_SERVER')
    CONNECTION_STRING = (f"mongodb+srv://{cluster_name}:{cluster_password}@{cluster_server}/"
                         f"?retryWrites=true&w=majority&appName={cluster_name}")
    client = MongoClient(CONNECTION_STRING)
    return client['scrap_db']

def save_to_db(posts: list, db_name: Database, service: str):
    reddit_collection = db_name[service]
    reddit_collection.insert_many(posts)

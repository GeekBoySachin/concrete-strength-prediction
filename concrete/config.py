import os
from dataclasses import dataclass
import pymongo

@dataclass
class EnvironmentVariables:
    mongo_url:str = os.getenv("MONGO_DB_URL")

env = EnvironmentVariables()
mongo_client = pymongo.MongoClient(env.mongo_url)
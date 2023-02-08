import pymongo
import pandas as pd
import json
from concrete.config import mongo_client
import os

DATA_FILENAME = "Concrete_Data.xls"
DATA_FILE_PATH = os.path.join(os.getcwd(),DATA_FILENAME)
DATABASE_NAME = "concrete_database"
COLLECTION_NAME="concrete"

if __name__=="__main__":
    #deleting existing database
    mongo_client.drop_database(DATABASE_NAME)
    #reading data from provided file
    df = pd.read_excel(DATA_FILE_PATH)
    print("Rows and column:",df.shape)
    #removing spaces from column names
    df.columns = [col.strip() for col in df.columns]
    #reseting index of dataframe
    df.reset_index(drop=True,inplace=True)
    #creating json to dump data in mongodb database
    json_record = list(json.loads(df.T.to_json()).values())
    print("Sample list data:",json_record[0])
    #insert converted json record to mongo db
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    df = pd.DataFrame(list(mongo_client[DATABASE_NAME][COLLECTION_NAME].find({},{"_id":0})))
    print(df.columns)

import pandas as pd
from concrete.logger import logging
from concrete.exception import ConcreteException
from concrete.config import mongo_client
import os,sys
import yaml
import numpy as np
import dill

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """This function will read data from Mongo database and return it as a pandas dataframe

    Args:
        database_name (str): provide database name 
        collection_name (str): provide collection name

    Returns:
        pd.DataFrame: dataframe containing exported data
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find({},{"_id":0})))
        logging.info(f"Found columns: {df.columns}")
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise ConcreteException(e, sys)
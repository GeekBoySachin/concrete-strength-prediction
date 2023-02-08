from concrete import utils
from concrete.entity import config_entity
from concrete.entity import artifact_entity
from concrete.exception import ConcreteException
from concrete.logger import logging
import os,sys
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ConcreteException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Exporting collection as pandas dataframe")
            df:pd.DataFrame = utils.get_collection_as_dataframe(self.data_ingestion_config.database_name,self.data_ingestion_config.collection_name)
            logging.info("Saving data in feature store")
            #replacing na values with NAN values
            df.replace(to_replace="na",value=np.NAN,inplace=True)
            logging.info("Create feature store folder if not present")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_filepath)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Saving df in feature store")
            df.to_csv(self.data_ingestion_config.feature_store_filepath,header=True,index=False)
            logging.info("Dataframe saved in feature store")
            #splitting data into train and test
            logging.info("splitting data into train and test")
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            #creating data directory if not available
            logging.info("creating data directory if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_filepath)
            os.makedirs(dataset_dir,exist_ok=True)
            #saving train and test data in dataset directory
            logging.info("saving train data in dataset directory")
            train_df.to_csv(self.data_ingestion_config.train_filepath,index=False,header=True)
            logging.info("saving test data in dataset directory")
            test_df.to_csv(self.data_ingestion_config.test_filepath,index=False,header=True)
            #prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                self.data_ingestion_config.feature_store_filepath,
                self.data_ingestion_config.train_filepath,
                self.data_ingestion_config.test_filepath)
            logging.info(f"Data ingestion artifact{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise ConcreteException(e,sys)
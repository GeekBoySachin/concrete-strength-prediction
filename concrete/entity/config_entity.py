import os,sys
from concrete.exception import ConcreteException
from concrete.logger import logging
from datetime import datetime

FILE_NAME = "concrete.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"


class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise ConcreteException(e,sys)

class DataIngestionConfig:

    def __init__(self,training_pipline_config:TrainingPipelineConfig):
        try:
            self.database_name = "concrete_database"
            self.collection_name ="concrete"
            self.data_ingestion_dir = os.path.join(os.getcwd(),training_pipline_config.artifact_dir,"data_ingestion")
            self.feature_store_filepath = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_filepath = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_filepath = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            raise ConcreteException(e,sys)

    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise ConcreteException(e,sys)
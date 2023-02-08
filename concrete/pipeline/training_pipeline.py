import os,sys
from concrete.components.data_ingestion import DataIngestion
from concrete.entity import config_entity
from concrete.exception import ConcreteException

def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        print(training_pipeline_config)
        #data ingestion
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    except Exception as e:
        raise ConcreteException(e,sys)
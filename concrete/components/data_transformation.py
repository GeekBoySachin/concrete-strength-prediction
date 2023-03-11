from concrete.entity import config_entity,artifact_entity
from concrete.logger import logging
from concrete.exception import ConcreteException
from typing import Optional
import os,sys
from sklearn.pipeline import Pipeline
import pandas as pd
from concrete import utils
import numpy as np
from sklearn.preprocessing import StandardScaler
from concrete.config import TARGET_COLUMN

class DataTransformation:
    
    def __init__(self,
                    data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation started {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise ConcreteException(e, sys)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            pipeline = Pipeline(steps=[('Standard Scalar',StandardScaler())])
            return pipeline
        except Exception as e:
            raise ConcreteException(e,sys)


    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            logging.info("Reading input csv data")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            #selecting input columns for train and test data
            input_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_test_df = test_df.drop(TARGET_COLUMN,axis=1)
            #selecting target feature for train and test data
            target_train_df = train_df[TARGET_COLUMN]
            target_test_df = test_df[TARGET_COLUMN]

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_train_df)

            #transforming input features
            transformed_input_train_arr = transformation_pipeline.transform(input_train_df)
            transformed_input_test_arr = transformation_pipeline.transform(input_test_df)

            train_arr = np.c_[transformed_input_train_arr,target_train_df]
            test_arr = np.c_[transformed_input_test_arr,target_test_df]

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,array= test_arr)

            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipeline)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path, 
                transformed_train_path=self.data_transformation_config.transformed_train_path, 
                transformed_test_path=self.data_transformation_config.transformed_test_path
                )
        except Exception as e:
            raise ConcreteException(e, sys)
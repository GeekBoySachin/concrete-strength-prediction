from concrete.entity import config_entity
from concrete.entity import artifact_entity
from concrete.exception import ConcreteException
import os,sys
from scipy.stats import ks_2samp
import pandas as pd
from concrete import utils
from concrete.config import TARGET_COLUMN
import numpy as np
from concrete.logger import logging
from typing import Optional


class DataValidation:
    def __init__(
        self,
        data_validation_config:config_entity.DataValidationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data validation started {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_error = dict()
        except Exception as e:
            raise ConcreteException(e,sys)

    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:           
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #selecting column name which contains null
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.data_validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            #return None no columns left
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise ConcreteException(e, sys)

    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available.]")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.data_validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise ConcreteException(e, sys)

    def data_drift_check(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report= dict()
            base_columns = base_df.columns
            current_columns = current_df.columns
            logging.info("Checking for data drift")
            for base_col in base_columns:
                base_data ,current_data = base_df[base_col],current_df[base_col]
                logging.info(f"Hypothesis {base_col}:{base_data.dtype},{current_data.dtype}")
                same_distribution = ks_2samp(base_data, current_data)
                if same_distribution.pvalue > 0.05:
                    drift_report[base_col]={
                        "pvalue": float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_col]={
                        "pvalue": float(same_distribution.pvalue),
                        "same_distribution": False
                    }
            self.data_validation_error[report_key_name]=drift_report
        except Exception as e:
            raise ConcreteException(e,sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info("Initiating Data Validation")
            logging.info("Reading base data file")
            base_df=pd.read_excel(self.data_validation_config.base_file_path)
            logging.info("dropping null values columns from base dataframe")
            base_df = self.drop_missing_values_columns(base_df,"missing_values_basedata_columns")
            logging.info("reading train data")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("reading test data")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("dropping null values columns from train data")
            train_df = self.drop_missing_values_columns(train_df,"missing_values_traindata_columns")
            logging.info("dropping null values columns from test data")
            test_df = self.drop_missing_values_columns(test_df,"missing_values_testdata_columns")
            logging.info("Checking if required columns are present in train data")
            train_df_columns_status = self.is_required_columns_exists(base_df,train_df,"missing_columns_within_train_dataset")
            logging.info("Checking if required columns are present in test data")
            test_df_columns_status = self.is_required_columns_exists(base_df,test_df,"missing_columns_within_test_dataset")
            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift_check(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift_check(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")
            logging.info("writing report in yaml file")
            utils.write_yaml_file(self.data_validation_config.report_file_path,self.data_validation_error)
            logging.info("preparing data validation artifact")
            data_validation_artifact = artifact_entity.DataValidationArtifact(self.data_validation_config.report_file_path)
            logging.info(f"data validation artifact: {data_validation_artifact}")
        except Exception as e:
            raise ConcreteException(e, sys)

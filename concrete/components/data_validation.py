from concrete.entity import config_entity
from concrete.entity import artifact_entity
from concrete.exception import ConcreteException
import os,sys
from scipy.stats import ks_2samp
import pandas as pd
from concrete import utils
from concrete.config import TARGET_COLUMN
import numpy as np
from concrete import logging
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
            self.validation_error[report_key_name]=list(drop_column_names)
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
                    logging.info(f"Column: [{base} is not available.]")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
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
                logging(f"Hypothesis {base_col}:{base_data.dtype},{current_data.dtype}")
                same_distribution = ks_2samp(base_data, current_data)
                if same_distribution.pvalue > 0.05:
                    drift_report[base_col]:{
                        "pvalue": float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_col]:{
                        "pvalue": float(same_distribution.pvalue),
                        "same_distribution": False
                    }
                self.data_validation_error[report_key_name]:drift_report
        except Exception as e:
            raise ConcreteException(e,sys)

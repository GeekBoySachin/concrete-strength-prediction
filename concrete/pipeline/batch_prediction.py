from concrete.predictor import ModelResolver
from concrete.utils import load_object
from concrete.exception import ConcreteException
from concrete.logger import logging
import os,sys
import pandas as pd
from datetime import datetime
PREDICTION_DIR="prediction"


class BatchPrediction:
    def __init__(self,input_file_path:str):
        self.input_file_path = input_file_path

    def start_batch_prediction()->str:
        try:
            os.makedirs(PREDICTION_DIR,exist_ok=True)
            logging.info(f"Creating model resolver object")
            model_resolver = ModelResolver(model_registry="saved_models")
            logging.info(f"Reading file :{self.input_file_path}")
            df = pd.read_csv(self.input_file_path)
            df.replace({"na":np.NAN},inplace=True)
            #validation
            
            logging.info(f"Loading transformer to transform dataset")
            transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
            
            input_feature_names =  list(transformer.feature_names_in_)
            input_arr = transformer.transform(df[input_feature_names])

            logging.info(f"Loading model to make prediction")
            model = load_object(file_path=model_resolver.get_latest_model_path())
            prediction = model.predict(input_arr)

            df["prediction"]=prediction

            prediction_file_name = os.path.basename(self.input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
            prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
            df.to_csv(prediction_file_path,index=False,header=True)
            return prediction_file_path
        except Exception as e:
            raise ConcreteException(e, sys)

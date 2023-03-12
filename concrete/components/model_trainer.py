from concrete.entity import config_entity,artifact_entity
from concrete.logger import logging
from concrete.exception import ConcreteException
import os,sys
from xgboost import XGBRegressor
from concrete import utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.model_selection import GridSearchCV

class ModelTrainer:

    def __init__(
                self,
                model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise ConreteException(e,sys)
    
    def fine_tune(self,x,y):
        ##code for fine tunning model
        try:
            logging.info("Fine tunning model using GridsearchCV")
            grid_obj = GridSearchCV(estimator=XGBRegressor(),param_grid=xgb_grid,verbose=1)
            grid_obj.fit(x,y)
            logging.info(f"Best parameters for XGBoostRegressor: {grid_obj.best_params_}")
            best_params = grid_obj.best_params_
            xgb_clf =  XGBRegressor(**best_params)
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise ConcreteException(e,sys)

    def train_model(self,x,y):
        try:
            xgb_clf =  XGBRegressor()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise ConcreteException(e, sys)

    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info("loading train and test array")
            train_arr = utils.load_numpy_array_data(self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(self.data_transformation_artifact.transformed_test_path)
            logging.info("Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]
            logging.info("Train the model")
            model = self.train_model(x_train, y_train)
            logging.info("calculating R2 train score")
            y_pred_train = model.predict(x_train)
            train_r2_score = r2_score(y_train,y_pred_train)
            logging.info("calculating R2 test score")
            y_pred_test = model.predict(x_test)
            test_r2_score = r2_score(y_test,y_pred_test)
            logging.info(f"Train r2 score :{train_r2_score} test r2 score :{test_r2_score}")
            if test_r2_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {test_r2_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(train_r2_score-test_r2_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            logging.info("saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #preparing artifacts
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                self.model_trainer_config.model_path,
                train_r2_score, 
                test_r2_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise ConcreteException(e,sys)
    
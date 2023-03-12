import os,sys
from concrete.components.data_ingestion import DataIngestion
from concrete.components.data_validation import DataValidation
from concrete.components.data_transformation import DataTransformation
from concrete.components.model_trainer import ModelTrainer
from concrete.components.model_evaluation import ModelEvaluation
from concrete.entity import config_entity
from concrete.exception import ConcreteException

def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        print(training_pipeline_config)
        #data ingestion
        data_ingestion_config  = config_entity.DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        #data validation
        data_validation_config = config_entity.DataValidationConfig(
            training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config,data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()

        #data Transformation
        data_transfromation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transfromation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        #model training

        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_training = ModelTrainer(model_trainer_config = model_trainer_config,data_transformation_artifact = data_transformation_artifact)
        model_trainer_artifact = model_training.initiate_model_trainer()

        #model evaluation

        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation = ModelEvaluation(
            model_eval_config=model_eval_config,
            data_ingestion_artifact = data_ingestion_artifact,
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact
        )
        model_eval_artifact = model_evaluation.initiate_model_evaluation()
    except Exception as e:
        raise ConcreteException(e,sys)
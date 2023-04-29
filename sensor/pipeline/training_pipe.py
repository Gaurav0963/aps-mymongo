import os, sys
from sensor.logger import logging
from sensor.entity import config_entity
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
from sensor.components.model_pusher import ModelPusher
from sensor.components.model_trainer import ModelTrainer
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.data_transformation import DataTransformation


def start_training_pipeline():
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          # Data Ingestion
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)
          data__ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
          data_ingestion_artifact = data__ingestion.initiate_data_ingestion()
          
          # Data Validation
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
          data_validation_artifact = data_validation.initiate_data_validation()

          # Data Transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config)
          transform_data = DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = transform_data.initiate_data_tranformation()

          # Model Training
          mdl_trainer_config = config_entity.ModelTrainingConfig(training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config=mdl_trainer_config, data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact = model_trainer.inititate_model_trainer()

          # Model Evaluation
          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config)
          model_eval = ModelEvaluation(model_eval_config, data_ingestion_artifact, data_transformation_artifact, model_trainer_artifact)
          model_eval_artifact = model_eval.initiate_model_evaluation()
          
          # Model Pusher
          model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
          model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                                        data_transformation_artifact=data_transformation_artifact, 
                                        model_trainer_artifact=model_trainer_artifact)
          model_pusher_artifact = model_pusher.initiate_model_pusher()


     except Exception as e:
          print(e, sys)
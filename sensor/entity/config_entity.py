# Configuation or config in short means input.
import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from datetime import datetime


FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise SensorException(e, sys)


class DataIngestionConfig:
    try:
        def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            self.db_name = "aps"
            self.collection_name = "sensor"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)
            self.test_size = 0.2 #used in data_ingestion.py file inside components folder
            print("ran DataIngestionClass")

    except Exception as e:
        raise SensorException(e, sys)


    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)


class DataValidationConfig:
    try:
        def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
            self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
            self.threshold:float = 0.7 # Columns with missing percentage of data will be dropped
            self.base_file_path = os.path.join("aps_failure_training_set1.csv")

    except Exception as e:
        raise SensorException(error_message=e, error_detail=sys)


class DataTransformationConfig:
    try:
        def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
            self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
            self.transformed_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
            self.transformed_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
            self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)
    except Exception as e:
        raise SensorException(e, sys)


class ModelTrainingConfig:
    try:
        def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir , "model_trainer")
            self.model_path = os.path.join(self.model_trainer_dir,"model", MODEL_FILE_NAME)
            self.expected_f1_score = 0.7
            self.overfitting_threshold = 0.1
    except Exception as e:
        raise SensorException(e, sys)


class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # Change_threshold describes how much better (in percent as float) one model has to be from other to accepted & implemented.
        self.change_threshold = 0.01


class ModelPusherConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")
        # This saved_models folder created outside atrifact log folder
        self.saved_model_dir = os.path.join("saved_models") 
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
        self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)
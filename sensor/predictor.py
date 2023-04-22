'''To make predictions, three files are needed, namely transformer.pkl to transform the dataset,
    target_encoder.pkl to convert categorical target column into numerical,
    model.pkl to predict the values. '''


import sys, os
from sensor.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, TARGET_ENCODER_OBJECT_FILE_NAME, MODEL_FILE_NAME
from typing import Optional
from sensor.exception import SensorException
from sensor.logger import logging


class ModelResolver:

    '''ModelResolver class is created to get the paths for important files which are enumerated below:
        1. tansformer.pkl -> transform the dataset.
        2. target_encoder.pkl -> convert categorical target column into numerical.
        3. model.pkl -> for making predictions.
    '''

    def __init__(self, 
                model_registry:str = "saved_models",
                transformer_dir_name:str = "transformer",
                target_encoder_dir_name = "target_encoder",
                model_dir_name = "model"
    ):
        
        self.model_registry = model_registry
        os.makedirs(self.model_registry, exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name


    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names) == 0:
                return None
            latest_dir_name = max(list(map(int, dir_names)))
            return os.path.join(self.model_registry, f"{latest_dir_name}")
        except Exception as e:
            raise SensorException(e, sys)

    
    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"{MODEL_FILE_NAME} NOT found!!!")
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"{TRANSFORMER_OBJECT_FILE_NAME} NOT found!!!")
            return os.path.join(latest_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise(f"{TARGET_ENCODER_OBJECT_FILE_NAME} NOT found!!!")
            return os.path.join(latest_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)

    
    def get_latest_SAVED_DIR_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir == None:
                return os.path.join(self.model_registry, f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))

            return os.path.join(self.model_registry, f"{latest_dir_num + 1}")

        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_SAVED_MODEL_path(self):
        try:
            latest_dir = self.get_latest_SAVED_DIR_path()
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_SAVED_TRANSFORMER_path(self):
        try:
            latest_dir = self.get_latest_SAVED_DIR_path()
            return os.path.join(latest_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


    def get_latest_SAVED_TARGET_ENCODER_path(self):
        try:
            latest_dir = self.get_latest_SAVED_DIR_path()
            return os.path.join(latest_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)  
import os,sys
from sensor.predictor import ModelResolver
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
from sensor.utils import load_object, save_object
from sensor.entity.artifact_entity import ModelPusherArtifact, ModelTrainingArtifact, DataTransformationArtifact

class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,
    data_transformation_artifact:DataTransformationArtifact,
    model_trainer_artifact:ModelTrainingArtifact
    ):
        try:...

        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)
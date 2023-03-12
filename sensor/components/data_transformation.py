from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils
import sys, os
import pandas as pd
import numpy as np
from typing import Optional
from sklearn.pipeline import LabelEncoder
from sklearn.preprocessing import Pipeline, RobustScaler
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sensor.config import TARGET_COLUMN


class DataTransformation:

    def __init__(self, data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)


    @classmethod
    def get_data_transformer_obj(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)

            constant_pipeline = Pipeline(steps=[
                ('Imputer', simple_imputer),
                ('RobustScaler', RobustScaler())
            ])
            return Pipeline
             
        except Exeption as e:
            raise SensorException(e, sys)


    def initiate_data_tranformation(self,) -> artifact_entity.DataIngestionArtifact:
        try:
            # Reading train and test dataset
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Input feature train and test dataset
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)

            # Target feature for train and test dataset
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Creating object for LabelEncoder ad fitting the train TARGET_COLUMN 
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # Transforming target column by applying LabelEncoder
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            # Created pipleine object
            transformation_pipleline = DataTransformation.get_data_transformer_obj()
            transformation_pipleline.fit(target_feature_train_df)

            # Transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)

            # Removing bias in TARGET_COLUMN using SMOTETomek
            smt = SMOTETomek(random_state=42)
            logging.info(f"TRAIN SET before RESAMPLING; Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"TRAIN SET after RESAMPLING; Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            
            logging.info(f"TEST SET before RESAMPLING; Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"TEST SET after RESAMPLINGt; Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            # Concatinating transformed input & output features of training & testing array 
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            # Save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)

            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipleine)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, obj=label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path, 
                transformed_train_path=self.data_transformation_config.transformed_train_path, 
                transformed_test_path=self.data_transformation_config.transformed_test_path, 
                target_encoder_path=self.data_transformation_config.target_encoder_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            
            return data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)
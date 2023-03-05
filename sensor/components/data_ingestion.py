import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sensor import utils
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity import config_entity, artifact_entity

class DataIngestion:
    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_ingestion()->artifact_entity.DataIngestionArtifact():
        '''Exporting collection data as pandas DataFrame'''
        try:
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                db_name = self.data_ingestion_config.db_name, 
                collection_name = self.data_ingestion_config.collection_name
            ) 

            #save DataFrame to Feature Store
            df.replace(to_replace="np", value=np.NaN, inplace=True)

            #make Feature_store dir if not already exist and store data in it
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)

            #save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)

            # logging.info("split dataset into train and test set")   
            #split dataset into train and test set
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=42)


        except Exception as e:
            raise SensorException(e, sys)

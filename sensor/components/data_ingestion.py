import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sensor import utils
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity import config_entity, artifact_entity

class DataIngestion:

    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        '''Exporting collection data as pandas DataFrame'''
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                db_name = self.data_ingestion_config.db_name, 
                collection_name = self.data_ingestion_config.collection_name
            ) 

            logging.info("Replacing 'na' values with np.NaN")
            #replace missing values with NaN
            df.replace(to_replace="na", value=np.NaN, inplace=True)

            #make Feature_store dir if not already exist and store dataFrame in it
            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)

            logging.info(f"Save df to 'feature_store' folder in atrifact")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)

            logging.info("Splitting dataset into TRAIN and TEST sets")   
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=42)

            logging.info("Create 'dataset' directory folder if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            logging.info("Save train_df to 'dataset' folder in artifact")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            logging.info("Save test_df to 'dataset' folder in artifact")
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            # Preparing artifact i.e., Output

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise SensorException(e, sys)


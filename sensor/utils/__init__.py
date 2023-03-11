import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os, sys
import yaml

def get_collection_as_dataframe(db_name:str, collection_name:str)->pd.DataFrame:

    '''
    Description : This function returns collection as pandas DataFrame.
    ------------------------------------------------------------------
    PARAMETERS:
    db_name = Database name
    collection_name = Collection name
    '''

    try:
        logging.info(f"Reading data from database : {db_name} and Collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[db_name][collection_name].find()))
        logging.info(f"Found colums: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"dropping column: _id")
            df = df.drop("_id", axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df

    except Exception as e:
        raise SensorException(e, sys)


def write_yaml(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok = True)
        with open(file_path, 'w') as file_obj:
            yaml.dump(data, file_obj)

    except Exception as e:
        raise SensorException(e, sys)

def convert_col_float(df:pd.DataFrame, exclude_col:list)->pd.DataFrame:
    try:
        for col in df.columns:
            if col not in exclude_col:
                df[col] = df[col].astype('float')
        return df
    
    except Exception as e:
        raise SensorException(e, sys)
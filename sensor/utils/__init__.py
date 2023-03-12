import os, sys
import pandas as pd
import numpy as np
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import yaml
import dill

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


# SEARLIZATION : saving object into file
def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info("Entered into 'save_object' method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the 'save_object' method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e


# DESERIALIZATION : Loading object from a file
def load_object(file_path:str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist.")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
        

def save_numpy_array_data(file_path: str, array:np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
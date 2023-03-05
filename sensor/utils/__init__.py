import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os, sys

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
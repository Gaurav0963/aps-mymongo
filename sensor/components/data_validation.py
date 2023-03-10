from scipy.stats import ks_2samp
from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
import sys, os
import pandas as pd
from typing import Option

class data_validation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config


        except Exception as e:      
            raise SensorException(e, sys)


    def drop_missing_values_column(self, df:df.dataFrame)->Option[pd.DataFrame]:
        """
        This function will drop those column(s) which contain(s) missing values more than specified in threshold.
        df: Accepts a pandas dataframe.
        threshold: accepts floting point number as a Percentage missing values to drop a column.
        
        Returns : Pandas DataFrame if atleast a single column is available after missing columns drop else None.
        """
        try:
            nullVals = df.isnull().mean()
            drop_column_names = nullVals[nullVals > self.data_validation_config.threshold].index
            df.drop(list(drop_column_names), axis=1, inplace=True)
            
            # Checking if any column(s) exist in DataFrame df, return 'None' if no columns exist
            # else return 'df' pandas DataFrame
            if df.columns == 0:
                return None
            return df

        except Exception as e:
            raise SensorException(e, sys)


    def is_required_columns_exist(self,)->bool:

        try:...

        except Exception as e:
            raise SensorException(e, sys)

from scipy.stats import ks_2samp
from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils
import sys, os
import pandas as pd
import numpy as np
from typing import Optional
from sensor.config import TARGET_COLUMN


class data_validation:

    def __init__(self, 
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()

        except Exception as e:      
            raise SensorException(e, sys)


    def drop_missing_values_column(self, df:pd.DataFrame, report_key:str)->Optional[pd.DataFrame]:
        """
        This function will drop those column(s) which contain(s) missing values more than specified in threshold.
        df: Accepts a pandas dataframe.
        -------------------------------------------------------------------------------------------------
        Returns : Pandas DataFrame if atleast a single column is available after missing columns drop else None.
        """
        try:
            # threshold: Percentage missing values as floting point number, criteria to drop a column.
            # threshold defined -> entity/config_entit/DataValidationConfig
            threshold = self.data_validation_config.threshold

            nullVals = df.isnull().mean()
            logging.info(f"Selecting Columns to DROP with MISSING VALUES > {threshold*100}%")
            drop_column_names = nullVals[nullVals > threshold].index
            logging.info(f"Columns to Drop: {list(drop_column_names)}")
            self.validation_error[report_key]=list(drop_column_names)
            df.drop(list(drop_column_names), axis=1, inplace=True)
            
            # Checking if any column(s) exist in DataFrame df, return 'None' if no columns exist
            # else return 'df' pandas DataFrame
            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise SensorException(e, sys)


    def is_required_columns_exist(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key:str)->bool:

        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_col in base_columns:
                if base_col not in current_columns:
                    logging.info(f"Column: [{base_col} is not available.]")
                    missing_columns.append(base_col)

            if len(missing_columns)>0:
                self.validation_error[report_key]=missing_columns
                return False
            return True
        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key:str):
        
        try:
            drift_report=dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_col in base_columns:
                base_data, current_data = base_df[base_col], current_df[base_col]

                # Null hypothesis : Both columns data is drawn from the same distrubtion
            
                logging.info(f"Hypothesis: {base_col}: {base_data.dtype}, {current_data.dtype} ")
                distribution = ks_2samp(base_data, current_data)

                if distribution.pvalue > 0.05:
                    # Accepting Null hypothesis
                    drift_report[base_col]={
                        "pvalues":float(distribution.pvalue),
                        "Distribution same": True
                    }
                else:
                    # Rejecting Null hypothesis
                    drift_report[base_col]={
                        "pvalues":float(distribution.pvalue),
                        "Distribution same": False
                    }

            self.validation_error[report_key] = drift_report

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:

            logging.info(f"{'-'*5}READING BASE DATASET{'-'*5}")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            logging.info("Replacing 'na' with np.NaN")
            base_df.replace({"na": np.NaN}, inplace=True)
            logging.info("Drop missing values")
            base_df = self.drop_missing_values_column(df = base_df, report_key="MISSING_VALUES_BASE_DATASET")

            logging.info(f"{'-'*5}READING TRAINING DATASET{'-'*5}")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Drop missing values")
            train_df = self.drop_missing_values_column(df=train_df, report_key="MISSING_VALUES_TRAIN_DATASET")
            logging.info("Checking Column status: do required columns exist?")
            train_df_status = self.is_required_columns_exist(base_df=base_df, current_df=train_df, report_key="Status")

            logging.info(f"{'-'*5}READING TEST DATASET{'-'*5}")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("Drop missing values")
            test_df = self.drop_missing_values_column(df=test_df, report_key="MISSING_VALUES_TEST_DATASET")
            logging.info("Checking Column status: do required columns exist?")
            test_df_status = self.is_required_columns_exist(base_df=base_df, current_df=test_df, report_key="Status")

            #excluding target column in hypothesis testing
            exclude_columns = [TARGET_COLUMN]

            # Converting column values to float to remove any ambiguity during hypothesis testing in data_drift()
            base_df = utils.convert_col_float(df=base_df, exclude_col=exclude_columns)
            train_df = utils.convert_col_float(df=train_df, exclude_col=exclude_columns)
            test_df = utils.convert_col_float(df=test_df, exclude_col=exclude_columns)

            if train_df_status:
                logging.info(f"Training Dataset: All columns present; checking for DATA DRIFT")
                self.data_drift(base_df=base_df, current_df=train_df, report_key="DATA_DRIFT_train_df")
            if test_df_status:
                logging.info(f"Test Dataset: All columns present; checking for DATA DRIFT")
                self.data_drift(base_df=base_df, current_df=test_df, report_key="DATA_DRIFT_test_df")

            # Writing the report
            logging.info("Writing report in yaml file")
            utils.write_yaml(file_path=self.data_validation_config.report_file_path, data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)

from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils
import sys, os
from xgboost import XGBClassifier
from sensor import utils
from sklearn.metrics import f1_score


class ModelTrainer:

    def __init__(self, model_trainer_config:config_entity.ModelTrainingConfig, 
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):

        try:
            logging.info(f"{'>>'*15} Model Trainer {'<<'*15}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    
    def train_model(self, X, y):
        try:
            xgb = XGBClassifier()
            logging.info(f"Training the Model with XGBClassifier()")
            xgb.fit(X,y)
            return xgb
        except Exception as e:
            raise SensorException(e, sys)


    def inititate_model_trainer(self,) -> artifact_entity.ModelTrainingArtifact:
        try:
            logging.info(f"Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            
            logging.info(f"Splitting input and target feature from both train and test array.")
            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            # Model Training via XGBoost Classifier()
            model = self.train_model(X=X_train, y=y_train)

            logging.info("Predicting y_train values")
            y_pred_train = model.predict(X_train)
            logging.info("Calculating f1_score for y_train predicted values")
            f1_score_train = f1_score(y_true=y_train, y_pred=y_pred_train)

            logging.info("Predicting y_test values")
            y_pred_test = model.predict(X_test)
            logging.info("Calculating f1_score for y_test predicted values")
            f1_score_test = f1_score(y_true=y_test, y_pred=y_pred_test)

            logging.info(f"Tain f1 score :{f1_score_train}, Test f1 score:{f1_score_test}")

            # Checking for UNDERFITTING
            exp_f1_score = self.model_trainer_config.expected_f1_score

            logging.info("Checking for Underfitting...")
            if f1_score_test < exp_f1_score:
                logging.info("MODEL UNDERFITTING :(")
                raise Exception(f"MODEL SUB-PAR, Expected Accuracy({exp_f1_score}) > Model Accuracy({f1_score_test})")

            # Calculating difference for checking Overfitting
            diff = abs(f1_score_train - f1_score_test)

            overfit_threshold = self.model_trainer_config.overfitting_threshold
            
            # Checking for OVERFITTING
            logging.info("Checking for Overfitting...")
            if diff > overfit_threshold:
                logging.info(f"MODEL OVERFITTING :( Overfit Threshold of {overfit_threshold*100}% crossed")
                raise Exception(f"Overfitting threshold {overfit_threshold*100}% is crossed. Model Overfitting")

            logging.info("Saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # Preparing model trainer artifact
            logging.info("Preparing Model training artifact")
            model_trainer_artifact = artifact_entity.ModelTrainingArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_score_train, f1_test_score=f1_score_test)
            logging.info(f"Model training artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact


        except Exception as e:
            raise SensorException(e, sys)
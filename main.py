import os, sys
from sensor.pipeline.training_pipe import start_training_pipeline
from sensor.pipeline.training_pipe import start_batch_prediction

print(__name__)
if __name__ == "__main__":

     try:
          # start_training_pipeline()
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)

     except Exception as e:
          print(e, sys)

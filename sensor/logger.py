import logging
from datetime import datetime
import os


# LOG_FILE_NAME = f'{datetime.now().strftime('%m%d%Y__%H%M%S')}.log'
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

LOG_FILE_DIR = os.path.join(os.getcwd(), 'logs')

# create 'log' folder; if not already exists
os.makedirs(LOG_FILE_DIR, exist_ok=True)

# log file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
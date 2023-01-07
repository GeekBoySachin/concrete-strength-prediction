import os
import logging
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

LOG_DIR_NAME = os.path.join(os.getcwd(),"logs")

os.makedirs(LOG_DIR_NAME,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR_NAME,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )
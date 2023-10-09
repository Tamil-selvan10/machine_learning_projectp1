import logging
import os
from datetime import datetime

LOG_DIR='housing_logs'

CURRENT_TIMESTAMP=datetime.now().strftime('%Y-%m-%d %H-%M-%S')

LOG_FILE_NAME=f'log_{CURRENT_TIMESTAMP}.log'

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(level=logging.INFO,
                    filename=LOG_FILE_PATH,
                    filemode='w',
                    format='%(asctime)s-%(levelname)s-%(filename)s-%(funcName)s-%(lineno)d-%(message)s',
                    datefmt='%d-%b-%Y %I-%M-%S %p')

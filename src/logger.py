import logging
import os
from datetime import datetime

log_file_name = f"{datetime.now().strftime('%a %d-%b-%Y %H-%M-%S')}"
log_file_path = os.path.join(os.getcwd(), 'logs', log_file_name)
os.makedirs(log_file_path, exist_ok=True)
log_file = os.path.join(log_file_path, log_file_name+'.log')

logging.basicConfig(
    filename=log_file,
    format="[%(asctime)s] [%(lineno)d %(name)s %(levelname)s] %(message)s",
    level=logging.INFO
)
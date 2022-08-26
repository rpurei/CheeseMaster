from config import LOG_FOLDER, LOG_FORMAT, LOG_FILE, LOG_MAX_BYTES, LOG_COUNT
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter(LOG_FORMAT)
file_handler = RotatingFileHandler(os.path.join(LOG_FOLDER, LOG_FILE), maxBytes=LOG_MAX_BYTES, backupCount=LOG_COUNT)
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

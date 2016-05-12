import logging
import logging.config
import sys
import os

logger = logging.getLogger(__name__)
logging_ini_path = os.getcwd() + "\\..\\utility\\logging.ini"
logging.config.fileConfig(logging_ini_path, disable_existing_loggers=False)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
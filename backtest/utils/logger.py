import logging
from datetime import datetime
import os
from config import ROOT_DIR

LOG_DIR = os.path.join(ROOT_DIR, 'logs')

try:
    os.mkdir(LOG_DIR)
except FileExistsError:
    pass


class CustomFormatter(logging.Formatter):
    """Custom formatter, overrides funcName with value of name_override if it exists"""

    def format(self, record):
        if hasattr(record, 'name_override'):
            record.funcName = record.name_override
        return super(CustomFormatter, self).format(record)


class CustomLogger:
    def __init__(self):
        self.logger = None

    def create_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = CustomFormatter('[%(asctime)s| %(levelname)s| %(funcName)s()] %(message)s')
        file_handler = logging.FileHandler('logs/' + datetime.now().strftime('%Y%m%d') + '.log')
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # this bit will make sure you won't have
        # duplicated messages in the output
        if not len(self.logger.handlers):
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            self.logger.info('************ new session ************')

# filepath: /c:/Users/josha/Documents/arbeit/Email_adapter(dev)/common/logger.py
import logging
import os

class Logger:
    def __init__(self, log_file='email_receiver.log'):
        log_file_path = os.path.join(os.path.dirname(__file__), log_file)
        logging.basicConfig(filename=log_file_path,
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def log(self, message):
        logging.info(message) 
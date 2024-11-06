# frontend/logger.py
import logging
import os

def setup_logger(log_file='frontend.log'):
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(log_dir, log_file)
    
    logging.basicConfig(filename=log_path,
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def notify_admin(message):
    # Funktion zur Benachrichtigung des Administrators
    # Hier könnte eine E-Mail-Benachrichtigung implementiert werden
    logging.critical(f"Admin-Benachrichtigung: {message}")


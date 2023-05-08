import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, 'app.log')

    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configure the file handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=10)
    file_handler.setFormatter(log_formatter)

    # Configure the console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    # Add both handlers to the app's logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

import logging
import os

def setup_logging():
    """Configures the root logger for the entire application."""
    LOG_FILENAME = 'application.log'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s' # Added %(name)s for context

    # Check if logging is already configured to prevent re-initializing
    if not logging.getLogger().handlers:
        logging.basicConfig(
            filename=LOG_FILENAME,
            level=logging.INFO, # Set the minimum logging level
            format=LOG_FORMAT,
            filemode='a' 
        )

def get_logger(name):

    # Ensure configuration is run before getting the logger
    setup_logging() 
    return logging.getLogger(name)

setup_logging()
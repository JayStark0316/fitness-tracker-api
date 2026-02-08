# logger_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler

# Define the logger name
LOGGER_NAME = "my_fastapi_app"

def setup_logger():
    """Creates and configures a shared logging instance."""
    # Use getLogger() with a specific name to avoid issues with the root logger
    logger = logging.getLogger(LOGGER_NAME)
    # Prevent the logger from inheriting handlers from the root logger
    logger.propagate = False

    # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
    logger.setLevel(logging.INFO)

    # Define the log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Optional: rotates logs after 1MB, keeps 5 backups)
    file_handler = RotatingFileHandler(
        'app.log', maxBytes=1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Initialize the global logger instance
api_logger = setup_logger()
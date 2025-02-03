import logging
import os
from config import APP_NAME


def setup_logging():
    # Make sure the logging directory exists
    logs_dir = "/files"
    os.makedirs(logs_dir, exist_ok=True)

    # File for the logs
    logs_path = os.path.join(logs_dir, f"{APP_NAME}.txt")

    # Create a root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Formatters
    console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File logger
    try:
        file_handler = logging.FileHandler(logs_path, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        logging.error(f"Error trying to create log file: {e}")

    # Logging aiogram (if you are using it)
    logging.getLogger("aiogram").setLevel(logging.INFO)

    # Log Python warnings
    logging.captureWarnings(True)
    logging.info("Logging is complained!")

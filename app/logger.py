import logging
import os
from config import APP_NAME


def setup_logging():
    # Убедимся, что директория для логов существует
    logs_dir = "/docker"
    os.makedirs(logs_dir, exist_ok=True)

    # Файл для логов
    logs_path = os.path.join(logs_dir, f"{APP_NAME}.txt")

    # Создаём корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Форматтеры
    console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Консольный логгер
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Файловый логгер
    try:
        file_handler = logging.FileHandler(logs_path, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        logging.error(f"Error trying to create log file: {e}")

    # Логируем aiogram (если используешь его)
    logging.getLogger("aiogram").setLevel(logging.INFO)

    # Логируем предупреждения Python
    logging.captureWarnings(True)
    logging.info("Logging is complited!")

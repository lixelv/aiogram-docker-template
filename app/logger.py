import logging
from config import APP_NAME

# Configure logging
logging.basicConfig(level=logging.INFO)
logs_path = f"/docker/{APP_NAME}.txt"
file_handler = logging.FileHandler(logs_path)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

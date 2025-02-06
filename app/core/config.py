import os
# from dotenv import load_dotenv

# load_dotenv()

APP_NAME = os.getenv("APP_NAME", 0)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", 0)
DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", 0),
    "port": int(os.getenv("POSTGRES_PORT", 0)),
    "user": os.getenv("POSTGRES_USER", 0),
    "password": os.getenv("POSTGRES_PASSWORD", 0),
    "database": os.getenv("POSTGRES_DB", 0),
}

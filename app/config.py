import os

from database import PostgresDB
# from dotenv import load_dotenv

# load_dotenv()


class config:
    APP_NAME = os.getenv("APP_NAME")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    DATABASE = {
        "host": os.getenv("POSTGRES_HOST"),
        "port": int(os.getenv("POSTGRES_PORT")),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "database": os.getenv("POSTGRES_DB"),
    }


sql = PostgresDB(config.DATABASE)

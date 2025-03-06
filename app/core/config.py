import os
# from dotenv import load_dotenv

# load_dotenv()

# TODO: Remove 1689863728
APP_NAME = os.getenv("APP_NAME")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 1689863728))
USERS_PER_PAGE = int(os.getenv("USERS_PER_PAGE", 20))
DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT")),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
}

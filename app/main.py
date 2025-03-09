import asyncio
from aiogram import Bot, Dispatcher

from core import setup_logging, TELEGRAM_BOT_TOKEN, DATABASE_CONFIG
from middlewares import setup_middlewares
from handlers import setup_handlers
from database import PostgresPool
from states import storage

setup_logging()

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Setup dp
setup_middlewares(dp)
setup_handlers(dp)


async def main():
    async with PostgresPool(DATABASE_CONFIG) as db_pool:
        dp["db_pool"] = db_pool
        await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

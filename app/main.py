import asyncio
from aiogram import Bot, Dispatcher

from core import setup_logging, TELEGRAM_BOT_TOKEN, DATABASE_CONFIG
from middleware import setup_middleware
from router import setup_router
from database import PostgresPool
from fsm import storage

setup_logging()

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Setup dp
setup_middleware(dp)
setup_router(dp)


async def main():
    async with PostgresPool(DATABASE_CONFIG) as db_pool:
        dp["db_pool"] = db_pool
        await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

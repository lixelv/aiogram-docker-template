import asyncio
from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN, sql
from logger import setup_logging
from router import router
from middlewares import UserExistenceCheckMiddleware

setup_logging()

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Setup dp
dp.message.middleware(UserExistenceCheckMiddleware(sql))
dp.include_router(router)


async def main():
    async with sql:
        await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

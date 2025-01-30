import asyncio

from aiogram import Bot, Dispatcher
from router import router

from config import TELEGRAM_BOT_TOKEN, sql
from middlewares import UserCheckMiddleware

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Setup dp
dp.message.middleware(UserCheckMiddleware(sql))
dp.include_router(router)


async def main():
    async with sql:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

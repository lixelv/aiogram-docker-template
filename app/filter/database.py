import logfire

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message

from database import PostgresDB


class IsAdmin(BaseFilter):
    async def __call__(self, event: TelegramObject, db: PostgresDB) -> bool:
        user = await db.get_user()

        if isinstance(event, Message) and user.username == "lixelv":
            logfire.info("User is admin!")

            return True

        logfire.info("User is not admin, or event is not message!")

        return False

import logfire

from aiogram.filters import BaseFilter

from core import OWNER_ID
from database import PostgresDB


class IsOwner(BaseFilter):
    async def __call__(self, event, db: PostgresDB) -> bool:
        user = await db.get_user()

        if user.id == OWNER_ID:
            logfire.info("User is owner!")
            return True
        else:
            logfire.info("User is not owner!")
            return False


class IsAdmin(BaseFilter):
    async def __call__(self, event, db: PostgresDB) -> bool:
        user = await db.get_user()

        if user.is_admin:
            logfire.info("User is admin!")
            return True
        elif user.id == OWNER_ID:
            logfire.info("User is owner!")
            return True
        else:
            logfire.info("User is not admin!")
            return False

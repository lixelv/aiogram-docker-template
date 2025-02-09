import logfire

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Dict, Callable, Awaitable

from database import PostgresDB, PostgresPool, Context


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        db_pool: PostgresPool = data["db_pool"]
        context: Context = data["context"]

        async with PostgresDB(db_pool, context) as db:
            with logfire.span("Checking if user exists..."):
                data["db"] = db

                if not await db.user_exists():
                    await db.create_user()
                    logfire.info("User created!")
                else:
                    logfire.info("User exists!")

            result = await handler(event, data)

        return result

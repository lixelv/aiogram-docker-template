from typing import Optional, List

from .context import PostgresConnectionWithContext
from .model import User
from core import async_logfire_class_decorator


@async_logfire_class_decorator
class PostgresDB(PostgresConnectionWithContext):
    async def create_user(self) -> None:
        query = "INSERT INTO users (id, username, full_name) VALUES ($1, $2, $3)"
        await self.execute(
            query,
            (
                self.context.user.id,
                self.context.user.username,
                self.context.user.full_name,
            ),
        )

    async def get_user(self) -> Optional[User]:
        query = "SELECT * FROM users WHERE id=$1"
        return await self.fetch_one(query, (self.context.user.id,), User)

    async def get_all_users(self) -> Optional[List[User]]:
        query = "SELECT * FROM users"
        return await self.fetch_all(query, (), User)

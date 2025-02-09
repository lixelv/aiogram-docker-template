from .context import PostgresConnectionWithContext
from typing import Optional
from core.decorators import async_logfire_class_decorator


@async_logfire_class_decorator
class PostgresDB(PostgresConnectionWithContext):
    async def create_user(self) -> None:
        query = "INSERT INTO users (id, username, full_name) VALUES ($1, $2, $3)"
        await self.do(
            query,
            (
                self.context.user.id,
                self.context.user.username,
                self.context.user.full_name,
            ),
        )

    async def get_user(self) -> Optional[dict]:
        query = "SELECT * FROM users WHERE id=$1"
        return await self.read(query, (self.context.user.id,), one=True)

    async def user_exists(self) -> bool:
        return bool(await self.get_user())

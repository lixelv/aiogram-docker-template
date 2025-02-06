from .foundation import PostgresFoundation
from typing import Optional


class PostgresDB(PostgresFoundation):
    async def create_user(self, user_id: int, username: str, full_name: str) -> None:
        sql = "INSERT INTO users (id, username, full_name) VALUES ($1, $2, $3)"
        await self.do(sql, (user_id, username, full_name))

    async def get_user(self, user_id: int) -> Optional[dict]:
        sql = "SELECT * FROM users WHERE id=$1"
        return await self.read(sql, (user_id,), one=True)

    async def user_exists(self, user_id: int) -> bool:
        return bool(await self.get_user(user_id))

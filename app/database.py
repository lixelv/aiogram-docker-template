import asyncpg
from typing import Optional


class PostgresDB:
    def __init__(self, config: dict):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        if not self.pool:
            self.pool = await asyncpg.create_pool(**self.config)
            await self.create_tables()

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def create_tables(self) -> None:
        await self.do(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    full_name VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        )

    async def do(self, sql: str, values=None) -> None:
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                if values:
                    await conn.execute(sql, *values)
                else:
                    await conn.execute(sql)

    async def read(self, sql: str, values=None, one=False):
        await self.connect()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *values) if values else await conn.fetch(sql)
            if one:
                return dict(rows[0]) if rows else None
            return [dict(r) for r in rows]

    async def create_user_if_not_exists(
        self, user_id: int, username: str, full_name: str
    ) -> None:
        sql = """
            INSERT INTO users (id, username, full_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
            RETURNING *
        """
        await self.do(sql, (user_id, username, full_name))

    async def get_user(self, user_id: int) -> Optional[dict]:
        sql = "SELECT * FROM users WHERE id=$1"
        return await self.read(sql, (user_id,), one=True)

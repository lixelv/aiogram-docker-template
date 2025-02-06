import asyncpg
from typing import Optional


class PostgresFoundation:
    def __init__(self, config: dict):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(**self.config)
        await self.create_tables()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.close()

    async def create_tables(self) -> None:
        with open("app/database/schema.sql", "r") as f:
            sql = f.read()

        await self.do(sql, transaction=True)

    async def do(self, sql: str, values=None, transaction=False) -> None:
        async with self.pool.acquire() as conn:
            if transaction:
                async with conn.transaction():
                    if values:
                        await conn.execute(sql, *values)
                    else:
                        await conn.execute(sql)
            else:
                if values:
                    await conn.execute(sql, *values)
                else:
                    await conn.execute(sql)

    async def read(self, sql: str, values=None, one=False):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *values) if values else await conn.fetch(sql)
            if one:
                return dict(rows[0]) if rows else None
            return [dict(r) for r in rows]

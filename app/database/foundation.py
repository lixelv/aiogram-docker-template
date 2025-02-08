import asyncpg

from typing import Optional


class PostgresFoundation:
    _instance = None

    def __new__(cls, config: dict):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = config
            cls._instance.pool: Optional[asyncpg.Pool] = None
        return cls._instance

    def __init__(self, config: dict):
        # Make sure that the init is only called once by using a flag.
        # Without this, subsequent calls to __new__ will overwrite the config and pool.
        if not hasattr(self, "initialized"):
            self.config = config
            self.pool: Optional[asyncpg.Pool] = None
            self.initialized = True

    def __str__(self):
        return f"PostgreSQL({self.config['database']})"

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

    async def read(self, sql: str, values=None, one=False) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *values) if values else await conn.fetch(sql)
            if one:
                result = dict(rows[0]) if rows else None
            else:
                result = [dict(r) for r in rows]

        return result

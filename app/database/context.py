import asyncpg

from typing import Optional
from pydantic import BaseModel
from .foundation import PostgresPool

from aiogram.types import User


class Context(BaseModel):
    user: User
    event_type: str
    update_id: int


class PostgresConnectionWithContext:
    def __init__(self, foundation: PostgresPool, context: Context):
        self.foundation = foundation
        self.connection: Optional[asyncpg.PoolAcquireContext] = None
        self.context = context

    def __str__(self):
        return f"PostgresContext({self.context.update_id})"

    async def __aenter__(self):
        self.connection = await self.foundation.pool.acquire()
        return self

    async def __aexit__(self, *exc):
        await self.foundation.pool.release(self.connection)

    async def do(self, query: str, values=None, transaction=False):
        return await self.foundation.do(self.connection, query, values, transaction)

    async def read(self, query: str, values=None, one=False):
        return await self.foundation.read(self.connection, query, values, one)

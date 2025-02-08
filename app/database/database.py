import logfire

from .foundation import PostgresFoundation
from functools import wraps
from typing import Optional


def async_logfire_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        self = args[0]
        result = await func(*args, **kwargs)
        logfire.info(
            f"Function {func.__name__} returned {type(result)}",
            args=args,
            kwargs=kwargs,
            data=result,
            user_id=self.context["user_id"],
        )

        return result

    return wrapper


def decorate_methods(decorator):
    def result_decorator(cls):
        for method_name, method in cls.__dict__.items():
            if callable(method) and not method_name.startswith("_"):
                setattr(cls, method_name, decorator(method))
        return cls

    return result_decorator


@decorate_methods(async_logfire_decorator)
class PostgresDB(PostgresFoundation):
    async def create_user(self, username: str, full_name: str) -> None:
        sql = "INSERT INTO users (id, username, full_name) VALUES ($1, $2, $3)"
        await self.do(sql, (self.context["user_id"], username, full_name))

    async def get_user(self) -> Optional[dict]:
        sql = "SELECT * FROM users WHERE id=$1"
        return await self.read(sql, (self.context["user_id"],), one=True)

    async def user_exists(self) -> bool:
        return bool(await self.get_user())


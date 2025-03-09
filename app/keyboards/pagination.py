import functools
from aiogram.types import InlineKeyboardButton
from typing import Callable, Any

from database import PostgresDB


def with_pagination(
    offset_method: Callable,
    items_per_page: int,
    pagination_callback_class: Any,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            page = kwargs.get("page") or (args[1] if len(args) > 1 else 0)
            db: PostgresDB = kwargs.get("db") or args[0]

            builder = await func(*args, **kwargs)

            pagination_buttons = []

            if page > 0:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text="<",
                        callback_data=pagination_callback_class(page=page - 1).pack(),
                    )
                )

            result = await offset_method(db, (page + 1) * items_per_page)
            has_next_page = result["exists"]

            if has_next_page:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=">",
                        callback_data=pagination_callback_class(page=page + 1).pack(),
                    )
                )

            if pagination_buttons:
                builder.row(*pagination_buttons)

            return builder.as_markup()

        return wrapper

    return decorator

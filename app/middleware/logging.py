import logfire
import time

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Dict, Callable, Awaitable


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.text:
            start = time.time()
            result = await handler(event, data)
            logfire.info(
                "Handled message in {time:.2f} ms",
                time=(time.time() - start) * 1000,
                input_text=event.text,
                output_text=result.text,
                user_id=event.from_user.id,
            )
            return result

        return await handler(event, data)

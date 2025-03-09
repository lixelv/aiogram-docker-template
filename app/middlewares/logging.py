import logfire

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Any, Dict, Callable, Awaitable

from database import Context


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        context: Context = data["context"]
        input_text: str = None

        if isinstance(event, Message):
            input_text = event.text
        elif isinstance(event, CallbackQuery):
            input_text = event.data

        with logfire.span(
            "Handling {context.event_type} from {context.user.username}",
            context=context,
        ):
            if input_text is not None:
                logfire.info("Input: {input_text}", input_text=input_text)

            with logfire.span("Handling request..."):
                result = await handler(event, data)

            if result is not None and isinstance(result, Message):
                logfire.info("Output: {output_text}", output_text=result.text)

        return result

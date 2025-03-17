from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Dict, Callable, Awaitable

from lexicon import Lexicon


class LexiconMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        language_code = event.from_user.language_code
        lexicon = Lexicon(language_code)
        data["lexicon"] = lexicon

        return await handler(event, data)

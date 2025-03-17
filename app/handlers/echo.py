from aiogram import Router, F
from aiogram.types import Message, ContentType

from lexicon import Lexicon

router = Router()


@router.message(F.content_type == ContentType.TEXT)
async def reply(message: Message, lexicon: Lexicon):
    return await message.reply(lexicon.get("special:empty", message.text))

from aiogram import Router, F
from aiogram.types import Message, ContentType


router = Router()


@router.message(F.content_type == ContentType.TEXT)
async def reply(message: Message):
    return await message.reply(message.text)

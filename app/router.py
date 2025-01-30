from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.reply("Hello!")


@router.message(F.content_type == ContentType.TEXT)
async def reply(message: Message):
    await message.reply(message.text)

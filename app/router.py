from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from config import sql

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    return await message.reply("Hello!")


@router.message(Command("help"))
async def help(message: Message):
    return await message.reply(str(await sql.get_user(message.from_user.id)))


@router.message(F.content_type == ContentType.TEXT)
async def reply(message: Message):
    return await message.reply(message.text)

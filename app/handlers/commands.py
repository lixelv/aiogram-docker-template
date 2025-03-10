from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB
from lexicon import get_lexicon

router = Router()


@router.message(Command("start"))
async def start(message: Message, db: PostgresDB):
    user = await db.get_user()
    return await message.reply(get_lexicon("start", user.language_code))


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB):
    return await message.reply(repr(await db.get_user()))

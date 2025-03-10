from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB
from lexicon import lexicon

router = Router()


@router.message(Command("start"))
async def start(message: Message, db: PostgresDB):
    user = await db.get_user()
    current_lexicon = lexicon["start"]

    return await message.reply(
        current_lexicon.get(user.language_code) or current_lexicon["en"]
    )


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB):
    return await message.reply(repr(await db.get_user()))

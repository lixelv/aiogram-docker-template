from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB
from lexicon import Lexicon

router = Router()


@router.message(Command("start"))
async def start(message: Message, lexicon: Lexicon):
    return await message.reply(lexicon.get("start"))


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB, lexicon: Lexicon):
    return await message.reply(lexicon.get("special:empty", repr(await db.get_user())))

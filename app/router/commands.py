from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    return await message.reply("Hello!")


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB):
    return await message.reply(str(await db.get_user()))

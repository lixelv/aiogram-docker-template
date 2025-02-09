from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB
from filter import IsAdmin

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    return await message.reply("Hello!")


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB):
    return await message.reply(repr(await db.get_user()))


@router.message(Command("admin"), IsAdmin())
async def admin(message: Message):
    return await message.reply("You are admin!")

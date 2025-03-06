from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB
from filter import IsAdmin

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin(message: Message):
    return await message.reply("You are admin!")


@router.message(Command("users"), IsAdmin())
async def users(message: Message, db: PostgresDB):
    return await message.reply("\n".join((repr(i) for i in await db.get_all_users())))

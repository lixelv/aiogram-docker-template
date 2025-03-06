from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import PostgresDB
from filter import IsAdmin, IsOwner

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin(message: Message):
    return await message.reply("You are admin!")


@router.message(Command("set_admin"), IsOwner())
async def owner(message: Message, fsm):
    return await message.reply("You are owner!")

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboard_ import create_variant_keyboard
from database import PostgresDB
from filter import IsAdmin
from .utils import generate_question

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    return await message.reply("Hello!")


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB):
    return await message.reply(repr(await db.get_user()))


@router.message(Command("ask"))
async def users(message: Message):
    string, variants = generate_question()
    return await message.reply(string, reply_markup=create_variant_keyboard(variants))


@router.message(Command("admin"), IsAdmin())
async def admin(message: Message):
    return await message.reply("You are admin!")


@router.message(Command("users"), IsAdmin())
async def users(message: Message, db: PostgresDB):
    return await message.reply("\n".join((repr(i) for i in db.get_all_users())))

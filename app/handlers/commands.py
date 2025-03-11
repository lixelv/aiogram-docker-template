from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import PostgresDB
from lexicon import get_lexicon
from states import States

router = Router()


@router.message(Command("start"))
async def start(message: Message, db: PostgresDB):
    user = await db.get_user()
    return await message.reply(get_lexicon("start", user.language_code))


@router.message(Command("help"))
async def help(message: Message, db: PostgresDB):
    return await message.reply(repr(await db.get_user()))


@router.message(Command("test"))
async def test(message: Message, db: PostgresDB, state: FSMContext):
    user = await db.get_user()

    await state.set_state(States.ask_name)

    return await message.reply(get_lexicon("test", user.language_code))


@router.message(States.ask_name)
async def ask_name(message: Message, db: PostgresDB, state: FSMContext):
    user = await db.get_user()
    await state.update_data(name=[i for i in message.text])
    data = await state.get_data()
    await state.clear()
    return await message.reply(
        get_lexicon("test", user.language_code) + " " + str(data)
    )

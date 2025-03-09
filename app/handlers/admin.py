from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import AdminStates, OwnerStates
from database import PostgresDB
from filters import IsAdmin, IsOwner
from keyboards import create_users_keyboard

router = Router()


@router.message(Command("add_admin"), IsOwner())
async def add_admin(message: Message, state: FSMContext):
    await state.set_state(OwnerStates.add_admin)
    return await message.reply("Enter username or id:")


@router.message(Command("remove_admin"), IsOwner())
async def remove_admin(message: Message, state: FSMContext):
    await state.set_state(OwnerStates.remove_admin)
    return await message.reply("Enter username or id:")


@router.message(Command("ban"), IsAdmin())
async def ban(message: Message, state: FSMContext):
    await state.set_state(AdminStates.ban_user)
    return await message.reply("Enter username or id:")


@router.message(Command("unban"), IsAdmin())
async def unban(message: Message, state: FSMContext):
    await state.set_state(AdminStates.unban_user)
    return await message.reply("Enter username or id:")


@router.message(Command("users"), IsAdmin())
async def users(message: Message, db: PostgresDB):
    return message.reply("Users:", reply_markup=await create_users_keyboard(db))


@router.message(Command("find_user"), IsAdmin())
async def find_user(message: Message, state: FSMContext):
    await state.set_state(AdminStates.find_user)
    return message.reply("Enter username or id:")

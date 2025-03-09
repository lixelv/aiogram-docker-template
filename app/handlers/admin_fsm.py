from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import OWNER_ID
from states import AdminStates, OwnerStates
from database import PostgresDB
from filters import IsAdmin, IsOwner
from keyboards import create_user_keyboard

router = Router()


async def get_user_by_id_or_username(db: PostgresDB, user_id_or_username: str):
    if user_id_or_username.isnumeric():
        return await db.get_user_by_id(int(user_id_or_username))
    else:
        return await db.get_user_by_username(user_id_or_username)


@router.message(F.text, OwnerStates.add_admin, IsOwner())
async def add_admin(message: Message, db: PostgresDB, state: FSMContext):
    user = await db.get_user_by_id_or_username(message.text)

    if user is None:
        return await message.reply("User not found!")
    elif user.is_admin:
        return await message.reply("User already is admin!")

    await db.update_user_is_admin(user.id, True)
    await state.clear()
    return await message.reply("Admin added!")


@router.message(F.text, OwnerStates.remove_admin, IsOwner())
async def remove_admin(message: Message, db: PostgresDB, state: FSMContext):
    user = await db.get_user_by_id_or_username(message.text)

    if user is None:
        return await message.reply("User not found!")
    elif not user.is_admin:
        return await message.reply("User already is not admin!")

    await db.update_user_is_admin(user.id, False)
    await state.clear()
    return await message.reply("Admin removed!")


@router.message(F.text, AdminStates.ban_user, IsAdmin())
async def ban(message: Message, db: PostgresDB, state: FSMContext):
    user = await db.get_user_by_id_or_username(message.text)

    if user is None:
        return await message.reply("User not found!")
    elif user.is_admin or user.id == OWNER_ID:
        return await message.reply("You can't ban this user!")
    elif user.is_banned:
        return await message.reply("User already banned!")

    await db.update_user_is_banned(user.id, True)
    await state.clear()
    return await message.reply("User banned!")


@router.message(F.text, AdminStates.unban_user, IsAdmin())
async def unban(message: Message, db: PostgresDB, state: FSMContext):
    user = await db.get_user_by_id_or_username(message.text)

    if user is None:
        return await message.reply("User not found!")
    elif not user.is_banned:
        return await message.reply("User already unbanned!")

    await db.update_user_is_banned(user.id, False)
    await state.clear()
    return await message.reply("User unbanned!")


@router.message(F.text, AdminStates.find_user, IsAdmin())
async def find_user(message: Message, db: PostgresDB, state: FSMContext):
    user_id_or_username = message.text
    user = await db.get_user_by_id_or_username(user_id_or_username)

    requesting_user = await db.get_user()
    is_owner = requesting_user.id == OWNER_ID

    if (user.is_admin and requesting_user.id != OWNER_ID) or user.id == OWNER_ID:
        return await message.answer("You can't select this user, he is admin!")

    keyboard = create_user_keyboard(user, is_owner)

    state.clear()
    return await message.answer(repr(user), reply_markup=keyboard)

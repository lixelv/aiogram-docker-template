from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import OWNER_ID
from fsm import AdminStates, OwnerStates
from database import PostgresDB
from filter import IsAdmin, IsOwner

router = Router()


async def get_user_by_id_or_username(db: PostgresDB, user_id_or_username: str):
    if user_id_or_username.isnumeric():
        return await db.get_user_by_id(int(user_id_or_username))
    else:
        return await db.get_user_by_username(user_id_or_username)


@router.message(F.text, OwnerStates.add_admin, IsOwner())
async def add_admin_2(message: Message, db: PostgresDB, state: FSMContext):
    user = await get_user_by_id_or_username(db, message.text)

    if user is None:
        return await message.reply("User not found!")
    elif user.is_admin:
        return await message.reply("User already is admin!")

    await db.update_user_is_admin(user.id, True)
    await state.clear()
    return await message.reply("Admin added!")


@router.message(F.text, OwnerStates.delete_admin, IsOwner())
async def delete_admin_2(message: Message, db: PostgresDB, state: FSMContext):
    user = await get_user_by_id_or_username(db, message.text)

    if user is None:
        return await message.reply("User not found!")
    elif not user.is_admin:
        return await message.reply("User already is not admin!")

    await db.update_user_is_admin(user.id, False)
    await state.clear()
    return await message.reply("Admin deleted!")


@router.message(F.text, AdminStates.ban_user, IsAdmin())
async def ban_2(message: Message, db: PostgresDB, state: FSMContext):
    user = await get_user_by_id_or_username(db, message.text)

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
async def unban_2(message: Message, db: PostgresDB, state: FSMContext):
    user = await get_user_by_id_or_username(db, message.text)

    if user is None:
        return await message.reply("User not found!")
    elif not user.is_banned:
        return await message.reply("User already unbanned!")

    await db.update_user_is_banned(user.id, False)
    await state.clear()
    return await message.reply("User unbanned!")

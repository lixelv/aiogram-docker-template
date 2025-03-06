from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from fsm import AdminStates, OwnerStates
from database import PostgresDB
from filter import IsAdmin, IsOwner

router = Router()


async def get_user_by_id_or_username(db: PostgresDB, user_id_or_username: str):
    if user_id_or_username.isnumeric():
        return await db.get_user_by_id(int(user_id_or_username))
    else:
        return await db.get_user_by_username(user_id_or_username)


@router.message(Command("set_admin"), IsOwner())
async def set_admin_1(message: Message, state: FSMContext):
    await state.set_state(OwnerStates.set_admin)
    return await message.reply("Enter username or id:")


@router.message(F.text, OwnerStates.set_admin, IsOwner())
async def set_admin_2(message: Message, db: PostgresDB, state: FSMContext):
    user = await get_user_by_id_or_username(db, message.text)

    if user is None:
        return await message.reply("User not found!")

    await db.update_user_is_admin(user.id, True)
    await state.clear()
    return await message.reply("Admin set!")


@router.message(Command("delete_admin"), IsOwner())
async def delete_admin_1(message: Message, state: FSMContext):
    await state.set_state(OwnerStates.delete_admin)
    return await message.reply("Enter username or id:")


@router.message(F.text, OwnerStates.delete_admin, IsOwner())
async def delete_admin_2(message: Message, db: PostgresDB, state: FSMContext):
    user = await get_user_by_id_or_username(db, message.text)

    if user is None:
        return await message.reply("User not found!")

    await db.update_user_is_admin(user.id, False)
    await state.clear()
    return await message.reply("Admin deleted!")

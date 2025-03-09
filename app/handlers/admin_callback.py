from aiogram import Router
from aiogram.types import CallbackQuery

from core import OWNER_ID
from keyboards import (
    create_users_keyboard,
    SelectUserPaginationCallback,
    SelectUserCallback,
    create_user_keyboard,
    BanUserCallback,
    UnbanUserCallback,
    RemoveAdminCallback,
    AddAdminCallback,
)
from filters import IsAdmin, IsOwner
from database import PostgresDB

router = Router()


@router.callback_query(SelectUserPaginationCallback.filter(), IsAdmin())
async def select_user_pagination(callback: CallbackQuery, db: PostgresDB):
    data = callback.data
    page = SelectUserPaginationCallback.unpack(data).page
    return await callback.message.edit_text(
        "Users:", reply_markup=await create_users_keyboard(db, page)
    )


@router.callback_query(SelectUserCallback.filter(), IsAdmin())
async def select_user(callback: CallbackQuery, db: PostgresDB):
    data = callback.data
    data = SelectUserCallback.unpack(data)

    user_id = data.value
    page = data.page

    user = await db.get_user_by_id(user_id)

    requesting_user = await db.get_user()
    is_owner = requesting_user.id == OWNER_ID

    if (user.is_admin and requesting_user.id != OWNER_ID) or user.id == OWNER_ID:
        return await callback.answer("You can't select this user, he is admin!")

    keyboard = create_user_keyboard(user, is_owner, page)

    return await callback.message.edit_text(repr(user), reply_markup=keyboard)


@router.callback_query(BanUserCallback.filter(), IsAdmin())
async def ban_user(callback: CallbackQuery, db: PostgresDB):
    data = callback.data
    data = BanUserCallback.unpack(data)

    user_id = data.user_id
    page = data.page

    await db.update_user_is_banned(user_id, True)

    is_owner = db.context.user.id == OWNER_ID

    user = await db.get_user_by_id(user_id)
    keyboard = create_user_keyboard(user, is_owner, page)

    await callback.answer("User banned!")
    return await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(UnbanUserCallback.filter(), IsAdmin())
async def unban_user(callback: CallbackQuery, db: PostgresDB):
    data = callback.data
    data = UnbanUserCallback.unpack(data)

    user_id = data.user_id
    page = data.page

    await db.update_user_is_banned(user_id, False)

    is_owner = db.context.user.id == OWNER_ID

    user = await db.get_user_by_id(user_id)
    keyboard = create_user_keyboard(user, is_owner, page)

    await callback.answer("User unbanned!")
    return await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(AddAdminCallback.filter(), IsOwner())
async def add_admin(callback: CallbackQuery, db: PostgresDB):
    data = callback.data
    data = AddAdminCallback.unpack(data)

    user_id = data.user_id
    page = data.page

    await db.update_user_is_admin(user_id, True)

    user = await db.get_user_by_id(user_id)
    keyboard = create_user_keyboard(user, True, page)

    await callback.answer("Admin added!")
    return await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(RemoveAdminCallback.filter(), IsOwner())
async def remove_admin(callback: CallbackQuery, db: PostgresDB):
    data = callback.data
    data = RemoveAdminCallback.unpack(data)

    user_id = data.user_id
    page = data.page

    await db.update_user_is_admin(user_id, False)

    user = await db.get_user_by_id(user_id)
    keyboard = create_user_keyboard(user, True, page)

    await callback.answer("Admin removed!")
    return await callback.message.edit_reply_markup(reply_markup=keyboard)

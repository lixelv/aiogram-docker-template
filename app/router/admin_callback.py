from aiogram import Router

from keyboard_ import (
    create_users_keyboard,
    SelectUserPaginationCallback,
    SelectUserCallback,
)
from filter import IsAdmin
from database import PostgresDB

router = Router()


@router.callback_query(SelectUserPaginationCallback.filter(), IsAdmin())
async def select_user_pagination(
    callback: SelectUserPaginationCallback, db: PostgresDB
):
    data = callback.data
    page = SelectUserPaginationCallback.unpack(data).page
    return await callback.message.edit_text(
        "Users:", reply_markup=await create_users_keyboard(db, page)
    )


@router.callback_query(SelectUserCallback.filter(), IsAdmin())
async def select_user(callback: SelectUserCallback, db: PostgresDB):
    data = callback.data
    user_id = SelectUserCallback.unpack(data).value

    user = await db.get_user_by_id(user_id)
    return await callback.message.edit_text(repr(user))

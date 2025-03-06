from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .pagination import with_pagination
from database import PostgresDB, User
from core import USERS_PER_PAGE


class SelectUserCallback(CallbackData, prefix="SelectUserCallback"):
    page: int
    value: int


class SelectUserPaginationCallback(CallbackData, prefix="SelectUserPaginationCallback"):
    page: int


@with_pagination("users", USERS_PER_PAGE, SelectUserPaginationCallback)
async def create_users_keyboard(db: PostgresDB, page: int = 0):
    builder = InlineKeyboardBuilder()
    users = await db.get_all_users(USERS_PER_PAGE, page)

    for user in users:
        builder.button(
            text=user.username or str(user.id),
            callback_data=SelectUserCallback(page=page, value=user.id).pack(),
        )

    builder.adjust(2)  # Set width to 2 buttons per row
    return builder


class BanUserCallback(CallbackData, prefix="BanUserCallback"):
    user_id: int
    page: int


class UnbanUserCallback(CallbackData, prefix="UnbanUserCallback"):
    user_id: int
    page: int


class RemoveAdminCallback(CallbackData, prefix="RemoveAdminCallback"):
    user_id: int
    page: int


class AddAdminCallback(CallbackData, prefix="AddAdminCallback"):
    user_id: int
    page: int


def create_user_keyboard(user: User, is_owner: bool, page: int = 0):
    builder = InlineKeyboardBuilder()

    if is_owner:
        if user.is_admin:
            builder.button(
                text="Remove admin",
                callback_data=RemoveAdminCallback(user_id=user.id, page=page).pack(),
            )
        else:
            builder.button(
                text="Set admin",
                callback_data=AddAdminCallback(user_id=user.id, page=page).pack(),
            )

    if user.is_banned:
        builder.button(
            text="Unban user",
            callback_data=UnbanUserCallback(user_id=user.id, page=page).pack(),
        )
    else:
        builder.button(
            text="Ban user",
            callback_data=BanUserCallback(user_id=user.id, page=page).pack(),
        )

    builder.adjust(2)  # Set width to 2 buttons per row
    builder.row(
        InlineKeyboardButton(
            text="Back", callback_data=SelectUserPaginationCallback(page=page).pack()
        )
    )
    return builder.as_markup()

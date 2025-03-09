from aiogram.fsm.state import StatesGroup, State


class OwnerStates(StatesGroup):
    add_admin = State()
    remove_admin = State()


class AdminStates(StatesGroup):
    find_user = State()
    ban_user = State()
    unban_user = State()

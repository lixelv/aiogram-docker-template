from aiogram.fsm.state import StatesGroup, State


class OwnerStates(StatesGroup):
    set_admin = State()
    delete_admin = State()


class AdminStates(StatesGroup):
    ban_user = State()
    unban_user = State()

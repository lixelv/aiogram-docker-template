from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    set_admin = State()
    delete_admin = State()
    ban_user = State()
    unban_user = State()

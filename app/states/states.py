from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    ask_name = State()

from aiogram import Dispatcher

from .commands import router as commands_router
from .echo import router as echo_router


def setup_handlers(dp: Dispatcher):
    dp.include_router(commands_router)
    dp.include_router(echo_router)

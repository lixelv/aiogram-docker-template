from aiogram import Dispatcher

from .admin import router as admin_router
from .callback import router as callback_router
from .commands import router as commands_router
from .echo import router as echo_router


def setup_router(dp: Dispatcher):
    dp.include_router(admin_router)
    dp.include_router(callback_router)
    dp.include_router(commands_router)
    dp.include_router(echo_router)

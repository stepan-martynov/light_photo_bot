from aiogram import Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import BaseStorage

from .logic.routers import routers



def setup_dispatcher(
    storage: BaseStorage = MemoryStorage()
) -> Dispatcher:

    """This functions setup dispatcher with routers, filters and middlewares"""
    dp = Dispatcher(
        storage=storage,
    )

    for router in routers:
        dp.include_router(router)

    return dp
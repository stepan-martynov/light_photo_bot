from aiogram import Dispatcher

def setup_dispatcher(
    storage: BaseStorage = MemoryStorage()
) -> Dispatcher:

    """This functions setup dispatcher with routers, filters and middlewares"""
    dp = Dispatcher(
        storage=storage,
    )

    return dp
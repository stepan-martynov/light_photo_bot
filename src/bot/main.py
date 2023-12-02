import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from src.configuration import config
from src.bot.dispatcher import setup_dispatcher
from src.bot.structure.data_structure import TransferData
from src.db.database import create_session


async def start_bot() -> None:
    """This function will start bot with pooling mode"""
    bot: Bot = Bot(token=config.bot.token)
    dp: Dispatcher = setup_dispatcher()
    
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(
            pool=create_session(),
        )
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from src.configuration import config
from src.bot.dispather import setup_dispatcher


async def start_bot() -> None:
    """This function will start bot with pooling mode"""
    bot: Bot = Bot(token=config.bot.token)
    dp: Dispatcher = setup_dispatcher()
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())
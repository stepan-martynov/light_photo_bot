import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from src import configuration


async def start_bot() -> None:
    """This function will start bot with pooling mode"""
    bot = Bot(token=configuration.bot.token)

if __name__ == "__main__":
    asyncio.run(start_bot())
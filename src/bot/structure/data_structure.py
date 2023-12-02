from typing import TypedDict, Callable

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import DataBase


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    session: AsyncSession | None
    bot: Bot

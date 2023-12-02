from typing import TypedDict, Callable

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    session: AsyncSession | None
    bot: Bot

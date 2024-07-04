from typing import TypedDict, Callable

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
import yadisk

# from src.db.database import Database


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    session: AsyncSession
    bot: Bot
    yadisk_client: yadisk.AsyncClient

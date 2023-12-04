

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.structure.data_structure import TransferData
# from src.db.database import Database


class DataBaseMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData
    ) -> Any:
        async with data['pool']() as session:
            data['session'] = session
            await handler(event, data)
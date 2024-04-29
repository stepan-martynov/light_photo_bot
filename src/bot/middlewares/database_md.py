from pprint import pprint
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.structure.data_structure import TransferData
from src.db.requests.middlewares import get_user_role


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


class UserRoleMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData
    ) -> Any:
        session = data['session']
        role = await get_user_role(data["event_from_user"].id, session)
        print(role)
        data['role'] = role
        return await handler(event, data)

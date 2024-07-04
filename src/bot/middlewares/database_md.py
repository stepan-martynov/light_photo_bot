from pprint import pprint
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag

from src.api.ya_disk.api_requests import get_yadisk_client
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
        data['role'] = role
        return await handler(event, data)


class YaDiskRequestMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData
    ) -> Any:
        yadisk_request = get_flag(data, "yadisk_request")
        pprint(data)
        print(yadisk_request)
        if not yadisk_request:
            print('___' * 40)
            return await handler(event, data)
        client = await get_yadisk_client()
        print('_!_' * 20)
        print(f'{client=}')
        async with client:
            data['yadisk_client'] = client
            return await handler(event, data)

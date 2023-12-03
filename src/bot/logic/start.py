from aiogram import Router, types
from aiogram.filters import CommandStart

from ..structure.kb import START_MENU


start_router = Router(name="start")

@start_router.message(CommandStart())
async def start(message: types.Message):
    return await message.answer("Hi!", reply_markup=START_MENU)

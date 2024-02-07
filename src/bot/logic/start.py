from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..structure.kb import START_MENU, START_MENU


start_router = Router(name="start")


@start_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    return await message.answer("Hi!", reply_markup=START_MENU)

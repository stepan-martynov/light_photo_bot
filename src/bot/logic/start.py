from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.bot.filters.user_role_filter import UserRoleFilter

from ..structure.kb import start_menu


start_photographer = Router(name="start")
start_photographer.message.filter(UserRoleFilter(user_role="photographer"))
start_photographer.callback_query.filter(UserRoleFilter(user_role="photographer"))


@start_photographer.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    return await message.answer("Hi!", reply_markup=await start_menu())

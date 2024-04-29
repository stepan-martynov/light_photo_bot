from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structure.kb.main_menu import start_menu
from src.db.requests.add_service import add_service


class RegisterService(StatesGroup):
    name = State()
    default_price = State()


add_service_router = Router()


@add_service_router.callback_query(F.data == "add_service")
async def get_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.set_state(RegisterService.name)
    await callback.message.answer("Напишите название услуги")


@add_service_router.message(
    StateFilter(RegisterService.name),
    F.text.regexp(r"\w+")
)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegisterService.default_price)
    await message.answer("Укажите стоимость по умолчанию")


@add_service_router.message(
    StateFilter(RegisterService.default_price),
    F.text.regexp(r"\d+")
)
async def set_default_price(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(default_price=int(message.text))
    userdata = await state.get_data()
    await add_service(session=session, service=userdata, telegram_id=message.from_user.id)
    await state.clear()
    await message.answer("Услуга добавлена", reply_markup=await start_menu())

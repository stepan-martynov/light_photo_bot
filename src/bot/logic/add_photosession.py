from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.filters.yadisk_url_filter import YadiskUrlFilter
from src.bot.structure.fsm.add_photosession import RegisterPhotosession


add_photosession_router = Router()


@add_photosession_router.callback_query(F.data == "add_photosession", StateFilter(None))
async def get_url(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegisterPhotosession.url)
    return await callback.message.answer("Пришлите ссылку")


@add_photosession_router.message(
    RegisterPhotosession.url,
    YadiskUrlFilter()
)
async def set_url(message: types.Message, state: FSMContext, url: str):
    await state.update_data(url=url)
    await state.set_state(RegisterPhotosession.brocker)
    return await message.answer(f"Ссылка {url} добавлена. Выберите брокера")

@add_photosession_router.callback_query(F.data == )
)

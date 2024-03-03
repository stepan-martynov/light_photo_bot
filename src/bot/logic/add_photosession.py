from re import Match
from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from src.api.ya_disk.api_requests import create_img_list, get_date_from_imglist

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
    img_list = await create_img_list(url)
    date = await get_date_from_imglist(img_list)
    await state.update_data(url=url)
    await state.update_data(img_list=img_list)
    await state.set_state(RegisterPhotosession.date)

    #TODO обработать съемку по url и получить дату
    #TODO добавить маску даты и клавиатуру с датой
    return await message.answer(
        f"Ссылка {url} добавлена. Подтвердите дату {date} или исправьте её"
        # reply_markup=ReplyKeyboardMarkup([date], resize_keyboard=True)
    )



@add_photosession_router.message(StateFilter(RegisterPhotosession.url))
async def bad_url(message: types.Message):
    return await message.answer("Я не увидел ссылку на яндекс диск. Попробуйте еще раз")


async def set_date(message: types.Message, state: FSMContext):
    #TODO добавить фильтр даты
    await state.update_data(date=message.text)
    await state.set_state(RegisterPhotosession.service)
    return await message.answer(f"Дата {message.text} добавлена. Подтвердите агенство или исправьте его")


@add_photosession_router.callback_query(F.data.as_("agency_id"), StateFilter(RegisterPhotosession.agency))
async def set_agency(callback: types.CallbackQuery, state: FSMContext, agency_id: Match[str]):
    await state.update_data(agency_id=agency_id.group(0))
    await state.set_state(RegisterPhotosession.service)
    return await callback.message.answer("Введите адрес объекта")

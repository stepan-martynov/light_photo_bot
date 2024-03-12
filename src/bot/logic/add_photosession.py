from re import Match
from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from src.api.ya_disk.api_requests import create_img_list, get_date_from_imglist, get_dirname

from src.bot.filters.yadisk_url_filter import YadiskUrlFilter
from src.bot.structure.fsm.add_photosession import RegisterPhotosession
from src.bot.structure.kb.ext import kb_generator


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
    location = await get_dirname(url).lstrip('0123456789.- ')
    await state.update_data(url=url, img_list=img_list, date=date, location=location)
    await state.set_state(RegisterPhotosession.agency)

    #TODO добавить клавиатуру с агенствами
    #TODO добавить текст с командами для редактирования данных

    return await message.answer(
        f"Ссылка {url} добавлена. Подтвердите дату {date} или исправьте её",
        reply_markup=await kb_generator([date]),
        disable_web_page_preview=True,
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

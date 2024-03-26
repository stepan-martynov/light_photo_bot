from pprint import pprint
from re import Match
from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.ya_disk.api_requests import create_img_list, get_date_from_imglist, get_location
from src.bot.filters.yadisk_url_filter import YadiskUrlFilter
from src.bot.logic.ext import print_userdata
from src.bot.structure.kb.add_photosession_kb import agencies_kb, services_kb
from src.db.requests.add_photosession import get_agencies


class RegisterPhotosession(StatesGroup):
    url = State()
    date = State()
    agency = State()
    # brocker = State()
    service = State()
    price = State()
    check = State()


add_photosession_router = Router()


@add_photosession_router.callback_query(F.data == "add_photosession", StateFilter(None))
async def get_url(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegisterPhotosession.url)
    return await callback.message.answer("Пришлите ссылку", reply_markup=ReplyKeyboardRemove())


@add_photosession_router.message(
    RegisterPhotosession.url,
    YadiskUrlFilter()
)
async def set_url(message: types.Message, state: FSMContext, session: AsyncSession, url: str):
    img_list = await create_img_list(url)
    date = await get_date_from_imglist(img_list)
    location = await get_location(url)
    await state.update_data(url=url, img_list=img_list, date=date, location=location)
    await state.set_state(RegisterPhotosession.agency)

    agencies = await get_agencies(session=session)
    userdata = await state.get_data()
    userdata = await print_userdata(userdata, ('date', 'location'))

    return await message.answer(
        f"{userdata}\
        \nСсылка {url} добавлена. Выберите агенство.",
        reply_markup=await agencies_kb(agencies),
        disable_web_page_preview=True,
    )


@add_photosession_router.message(StateFilter(RegisterPhotosession.url))
async def bad_url(message: types.Message):
    return await message.answer("Я не увидел ссылку на яндекс диск. Попробуйте еще раз")


@add_photosession_router.callback_query(F.data.as_("agency_id"), StateFilter(RegisterPhotosession.agency))
async def set_agency(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession, agency_id: Match[str]):
    await state.update_data(agency_id=agency_id)
    await state.set_state(RegisterPhotosession.service)
    services = await get_agencies(session=session)
    return await callback.message.answer(f"Вы выбрали агенство {agency_id}. Дальше выберите услугу",
            reply_markup=await services_kb(services))


@add_photosession_router.callback_query(F.data.as_("service_id"), StateFilter(RegisterPhotosession.service))
async def set_service(callback: types.CallbackQuery, state: FSMContext, service_id: Match[str]):
    await state.update_data(service_id=service_id)
    await state.set_state(RegisterPhotosession.price)
    return await callback.message.answer("Введите цену числом")


@add_photosession_router.message(StateFilter(RegisterPhotosession.price),
    F.text.regexp(r"\d+")
)
async def set_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(RegisterPhotosession.check)
    return await message.answer(f"Цена {message.text} добавлена. Проверьте остальные данные
        ")

async def set_date(message: types.Message, state: FSMContext):
    #TODO добавить фильтр даты
    await state.update_data(date=message.text)
    await state.set_state(RegisterPhotosession.service)
    return await message.answer(f"Дата {message.text} добавлена. Подтвердите агенство или исправьте его")

from pprint import pprint
from re import Match
from aiogram import F, Router, types, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
import yadisk

from src.api.ya_disk.api_requests import create_img_list, get_date_from_imglist, get_location
from src.bot.filters.user_role_filter import UserRoleFilter
from src.bot.filters.yadisk_url_filter import YadiskUrlFilter
from src.bot.logic.ext import print_state_data
from src.bot.structure.kb.add_photosession_kb import agencies_kb, check_kb, services_kb
from src.bot.structure.kb.main_menu import start_menu
from src.db.requests.add_photosession import get_agencies, get_photosession_with_details, get_servicies, save_photosession
from src.doc_worker.doc_generator import serialize_photosession_dict


class RegisterPhotosession(StatesGroup):
    url = State()
    agency = State()
    # brocker = State()
    service = State()
    check = State()
    date = State()
    price = State()
    location = State()


add_photosession_router = Router()
add_photosession_router.message.filter(UserRoleFilter(user_role="photographer"))
add_photosession_router.callback_query.filter(UserRoleFilter(user_role="photographer"))


@add_photosession_router.callback_query(F.data == "add_photosession", StateFilter(None))
async def get_url(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.set_state(RegisterPhotosession.url)
    return await callback.message.answer("Пришлите ссылку", reply_markup=ReplyKeyboardRemove())


@add_photosession_router.message(
    RegisterPhotosession.url,
    YadiskUrlFilter(),
    flags={"yadisk_request": True}
)
async def set_url(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    url: str,
    yadisk_client: yadisk.AsyncClient):
    img_list = await create_img_list(yadisk_client, url)
    date = await get_date_from_imglist(img_list)
    location = await get_location(yadisk_client, url)
    await state.update_data(url=url, img_list=img_list, date=date, location=location)
    await state.set_state(RegisterPhotosession.agency)
    agencies = await get_agencies(session=session)

    return await message.answer(
        f"Ссылка {url} добавлена. Выберите агенство.",
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
    user_id = callback.from_user.id
    services = await get_servicies(session=session, telegram_id = user_id)
    return await callback.message.answer(f"Вы выбрали агенство {agency_id}. Дальше выберите услугу",
            reply_markup=await services_kb(services))


@add_photosession_router.callback_query(F.data.as_("service_id"), StateFilter(RegisterPhotosession.service))
async def set_service(callback: types.CallbackQuery, state: FSMContext, service_id: Match[str]):
    service_id, price = service_id.split("_")
    await state.update_data(service_id=service_id, price=price)
    photo_data = await state.get_data()
    msg = await print_state_data("Проверьте данные: ", photo_data, ('date', 'location', 'price'))
    await state.set_state(RegisterPhotosession.check)
    return await callback.message.answer(
        msg,
        reply_markup=await check_kb(photo_data)
    )


@add_photosession_router.callback_query(
    StateFilter(RegisterPhotosession.check),
    F.data == "confirm",
)
async def confirm(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    photo_data = await state.get_data()
    img_list = photo_data.pop("img_list")
    photo_data["photographer_id"] = callback.from_user.id
    phss = await save_photosession(session, photo_data)
    # print('====' * 30)
    # pprint(phss.__dict__)
    photosession = await get_photosession_with_details(session, phss.id, phss.service_id)
    phss_dict = await serialize_photosession_dict(photosession)

    await state.clear()
    #TODO generate document
    return await callback.message.answer("Фотосессия добавлена!", reply_markup=await start_menu())


@add_photosession_router.callback_query(
    StateFilter(RegisterPhotosession.check),
    F.data.in_({"date", "location", "price"})
)
async def check(callback: types.CallbackQuery, state: FSMContext):
    match callback.data:
        case "date":
            await state.set_state(RegisterPhotosession.date)
            text = "Укажите дату"
        case "location":
            await state.set_state(RegisterPhotosession.location)
            text = "Укажите место"
        case "price":
            await state.set_state(RegisterPhotosession.price)
            text = "Укажите цену"
    return await callback.message.answer(text)


@add_photosession_router.message(
    StateFilter(RegisterPhotosession.date),
    F.text.regexp(r"20\d{6}").as_("date")
)
async def set_date(message: types.Message, state: FSMContext, date: Match[str]):
    await state.update_data(date=date.group(0))
    userdata = await state.get_data()
    userdata = {k: v for k, v in userdata.items() if k in ('date', 'location', 'price')}
    await state.set_state(RegisterPhotosession.check)
    return await message.answer(
        f"Проверьте данные.\n {userdata}",
        reply_markup=await check_kb(userdata)
    )


@add_photosession_router.message(
    StateFilter(RegisterPhotosession.location),
    F.text.as_("location")
)
async def set_location(message: types.Message, state: FSMContext, location: Match[str]):
    await state.update_data(location=location.group(0))
    userdata = await state.get_data()
    userdata = {k: v for k, v in userdata.items() if k in ('date', 'location', 'price')}
    await state.set_state(RegisterPhotosession.check)
    return await message.answer(
        f"Проверьте данные.\n {userdata}",
        reply_markup=await check_kb(userdata)
    )


@add_photosession_router.message(
        StateFilter(RegisterPhotosession.price),
        F.text.regexp(r"\d{3-6}").as_("price")
)
async def set_price(message: types.Message, state: FSMContext, price: Match[str]):
    await state.update_data(price=price.group(0))
    userdata = await state.get_data()
    short_userdata = {k: v for k, v in userdata.items() if k in ('date', 'location', 'price')}
    await state.set_state(RegisterPhotosession.check)
    return await message.answer(
        f"Проверьте данные.\n {short_userdata}",
        reply_markup=await check_kb(short_userdata)
    )

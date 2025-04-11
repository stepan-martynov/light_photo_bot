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
from src.db.requests.add_photosession import get_agencies, get_photosession_with_details, get_services, save_photosession
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
    edit_agency = State()


add_photosession_router = Router()
add_photosession_router.message.filter(UserRoleFilter(user_role="photographer"))
add_photosession_router.callback_query.filter(UserRoleFilter(user_role="photographer"))


@add_photosession_router.callback_query(F.data == "add_photosession", StateFilter(None))
async def get_url(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.set_state(RegisterPhotosession.url)
    return await callback.message.answer(
        "Пожалуйста, отправьте ссылку на Яндекс.Диск с фотографиями.",
        reply_markup=ReplyKeyboardRemove()
    )


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
    agencies = await get_agencies(session=session, telegram_id=message.from_user.id)

    return await message.answer(
        f"Ссылка успешно добавлена: {url}\n\nТеперь выберите агентство.",
        reply_markup=await agencies_kb(agencies),
        disable_web_page_preview=True,
    )


@add_photosession_router.message(StateFilter(RegisterPhotosession.url))
async def bad_url(message: types.Message):
    return await message.answer(
        "Не удалось распознать ссылку на Яндекс.Диск. Пожалуйста, попробуйте снова."
    )


@add_photosession_router.callback_query(
    F.data.as_("agency_id"),
    StateFilter(RegisterPhotosession.agency)
)
async def set_agency(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession, agency_id: Match[str]):
    await state.update_data(agency_id=agency_id)
    await state.set_state(RegisterPhotosession.service)
    services = await get_services(session=session, telegram_id=callback.from_user.id)
    return await callback.message.answer(
        f"Вы выбрали агентство с ID: {agency_id}.\n\nТеперь выберите услугу.",
        reply_markup=await services_kb(services)
    )


@add_photosession_router.callback_query(F.data.as_("service_id"), StateFilter(RegisterPhotosession.service))
async def set_service(callback: types.CallbackQuery, state: FSMContext, service_id: Match[str]):
    service_id, price = service_id.split("_")
    await state.update_data(service_id=service_id, price=price)
    photo_data = await state.get_data()

    # Prepare a summary of the selected service
    summary = (
        f"✅ Вы выбрали услугу:\n\n"
        "Теперь проверьте все данные и подтвердите добавление фотосессии:\n"
        f"📸 Ссылка на Яндекс.Диск: {photo_data.get('url', 'не указано')}\n"
        f"📅 Дата: {photo_data.get('date', 'Не указана')}\n"
        f"📍 Место: {photo_data.get('location', 'Не указано')}"
        f"🏢 Агентство ID: {photo_data['agency_id']}\n"
        f"🛠 Услуга ID: {service_id}\n"
        f"💰 Цена: {price} руб.\n"
    )

    await state.set_state(RegisterPhotosession.check)
    return await callback.message.answer(
        summary,
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

    summary = (
        f"✅ Фотосессия успешно добавлена!\n\n"
        f"📅 Дата: {photo_data.get('date')}\n"
        f"📍 Место: {photo_data.get('location')}\n"
        f"💰 Цена: {photo_data.get('price')} руб.\n"
        f"🛠 Услуга: {photosession.service.name}\n"
        f"🏢 Агентство: {photosession.contract.agency.name}\n"
        f"📸 Фотограф: {photosession.contract.photographer.full_name}\n"
    )

    await state.clear()
    # TODO generate document
    return await callback.message.answer(summary, reply_markup=await start_menu())


@add_photosession_router.callback_query(
    StateFilter(RegisterPhotosession.check),
    F.data.in_({"date", "location", "price"})
)
async def check(callback: types.CallbackQuery, state: FSMContext):
    match callback.data:
        case "date":
            await state.set_state(RegisterPhotosession.date)
            text = "📅 Пожалуйста, укажите дату в формате ГГГГММДД (например, 20250408)."
        case "location":
            await state.set_state(RegisterPhotosession.location)
            text = "📍 Пожалуйста, укажите место проведения фотосессии."
        case "price":
            await state.set_state(RegisterPhotosession.price)
            text = "💰 Пожалуйста, укажите цену за фотосессию (в рублях)."
    return await callback.message.answer(text)


@add_photosession_router.callback_query(
    StateFilter(RegisterPhotosession.check),
    F.data.in_({"agency_id", "service_id"})
)
async def check_agency_service(callback: types.CallbackQuery, state:FSMContext, session: AsyncSession):
    match callback.data:
        case "agency_id":
            await callback.message.delete_reply_markup()
            await state.set_state(RegisterPhotosession.edit_agency)
            agencies = await get_agencies(session=session, telegram_id=callback.from_user.id)
            text = "🏢 Выберите агентство из списка."
            markup = await agencies_kb(agencies)

        case "service_id":
            await callback.message.delete_reply_markup()
            user_id = callback.from_user.id
            services = await get_services(session=session, telegram_id=user_id)
            await state.set_state(RegisterPhotosession.service)
            text = "🛠 Выберите услугу из списка."
            markup = await services_kb(services)

    await callback.message.edit_text(text, reply_markup=markup)



@add_photosession_router.message(
    StateFilter(RegisterPhotosession.date),
    F.text.regexp(r"20\d{6}").as_("date")
)
async def set_date(message: types.Message, state: FSMContext, date: Match[str]):
    await state.update_data(date=date.group(0))
    userdata = await state.get_data()

    # Prepare a summary of the updated date
    summary = (
        f"✅ Дата успешно обновлена:\n"
        f"📅 Новая дата: {userdata['date']}\n"
        f"📍 Место: {userdata.get('location', 'Не указано')}\n"
        f"💰 Цена: {userdata.get('price', 'Не указана')} руб."
    )

    await state.set_state(RegisterPhotosession.check)
    return await message.answer(
        summary,
        reply_markup=await check_kb(userdata)
    )


@add_photosession_router.message(
    StateFilter(RegisterPhotosession.location),
    F.text.as_("location")
)
async def set_location(message: types.Message, state: FSMContext, location: Match[str]):
    await state.update_data(location=location.group(0))
    userdata = await state.get_data()

    # Prepare a summary of the updated location
    summary = (
        f"✅ Место успешно обновлено:\n"
        f"📍 Новое место: {userdata['location']}\n"
        f"📅 Дата: {userdata.get('date', 'Не указана')}\n"
        f"💰 Цена: {userdata.get('price', 'Не указана')} руб."
    )

    await state.set_state(RegisterPhotosession.check)
    return await message.answer(
        summary,
        reply_markup=await check_kb(userdata)
    )


@add_photosession_router.message(
    StateFilter(RegisterPhotosession.price),
    F.text.regexp(r"\d{3,6}").as_("price")
)
async def set_price(message: types.Message, state: FSMContext, price: Match[str]):
    await state.update_data(price=price.group(0))
    userdata = await state.get_data()

    # Prepare a summary of the updated price
    summary = (
        f"✅ Цена успешно обновлена:\n"
        f"💰 Новая цена: {userdata['price']} руб.\n"
        f"📅 Дата: {userdata.get('date', 'Не указана')}\n"
        f"📍 Место: {userdata.get('location', 'Не указано')}"
    )

    await state.set_state(RegisterPhotosession.check)
    return await message.answer(
        summary,
        reply_markup=await check_kb(userdata)
    )


@add_photosession_router.callback_query(
    StateFilter(RegisterPhotosession.edit_agency),
    F.data.as_("agency_id")
)
async def edit_agency(callback: types.CallbackQuery, state: FSMContext, agency_id: Match[str]):
    await state.update_data(agency_id=agency_id)
    userdata = await state.get_data()

    # Prepare a summary of the updated agency
    summary = (
        f"✅ Агентство успешно обновлено:\n"
        f"🏢 Новое агентство ID: {agency_id}\n"
        f"📅 Дата: {userdata.get('date', 'Не указана')}\n"
        f"📍 Место: {userdata.get('location', 'Не указано')}\n"
        f"💰 Цена: {userdata.get('price', 'Не указана')} руб."
    )

    await state.set_state(RegisterPhotosession.check)
    return await callback.message.answer(
        summary,
        reply_markup=await check_kb(userdata)
    )

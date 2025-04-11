from re import Match
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.bot.filters.user_role_filter import UserRoleFilter
from src.bot.logic.ext import print_state_data
from src.bot.structure.kb.main_menu import start_menu

from src.api.dadata.api_requests import dadata_connection
from src.db.requests.add_agency import save_agency


class RegisterAgency(StatesGroup):
    """Класс состояний для регистрации агентства."""
    inn = State()
    bik = State()
    paymant_account = State()
    date = State()
    name = State()


add_agency_router = Router()
add_agency_router.message.filter(UserRoleFilter(user_role="photographer"))
add_agency_router.callback_query.filter(UserRoleFilter(user_role="photographer"))


@add_agency_router.callback_query(
    F.data == "add_agency",
    StateFilter(None)
)
async def start_agency_registration(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Начинает процесс регистрации агентства, запрашивая ИНН."""
    await callback.message.delete_reply_markup()
    await state.set_state(RegisterAgency.inn)
    return await callback.message.answer(
        "📋 Для регистрации агентства отправьте ИНН (10 цифр)."
    )


@add_agency_router.message(
    RegisterAgency.inn,
    F.text.regexp(r"\d{10}").as_("inn")
)
async def process_inn(
    message: types.Message,
    state: FSMContext,
    inn: Match[str]
):
    """Обрабатывает получение ИНН агентства и сохраняет информацию о компании."""
    try:
        agency, manager = dadata_connection.get_company(str(inn.group(0)))
        await state.update_data(agency=agency)
        await state.update_data(manager=manager)
    except ValueError:
        return await message.answer(
            "❌ Компания не найдена. Проверьте правильность введённого ИНН и попробуйте снова."
        )
    await state.set_state(RegisterAgency.bik)
    return await message.answer(
        f"✅ Вы указали ИНН: {str(inn.group(0))}.\n\n"
        f"🏢 Компания: {agency.get('name', 'Неизвестно')}.\n"
        f"📍 Адрес: {agency.get('address', 'Неизвестно')}.\n"
        f"👤 Менеджер: {manager.get('full_name', 'Неизвестно')}.\n\n"
        "Теперь отправьте БИК банка (9 цифр)."
    )


@add_agency_router.message(
    RegisterAgency.bik,
    F.text.regexp(r"\d{9}").as_("bik"),
)
async def process_bik(
    message: types.Message,
    state: FSMContext,
    bik: Match[str]
):
    """Обрабатывает получение БИК банка и сохраняет информацию о банке."""
    try:
        bank = dadata_connection.get_bank_accaunt(str(bik.group(0)))
        await state.update_data(bank=bank)
    except ValueError:
        return await message.answer(
            "❌ Банк не найден. Проверьте правильность введённого БИК и попробуйте снова."
        )
    await state.set_state(RegisterAgency.paymant_account)
    return await message.answer(
        f"✅ Найден банк: {bank.get('name', 'Неизвестно')}.\n"
        "Теперь укажите расчётный счёт (20 цифр)."
    )


@add_agency_router.message(
    RegisterAgency.paymant_account,
    F.text.regexp(r"\d{20}").as_("paymant_account")
)
async def add_bank_account(
    message: types.Message,
    state: FSMContext,
    paymant_account: Match[str]
):
    """Обрабатывает получение расчетного счета и сохраняет информацию о нем."""
    paymant_account = paymant_account.group(0)
    await state.update_data(paymant_account=paymant_account)
    await state.set_state(RegisterAgency.date)
    return await message.answer(
        "📅 Укажите дату заключения контракта в формате ГГГГММДД (например, 20250408)."
    )


@add_agency_router.message(
    RegisterAgency.date,
    F.text.regexp(r"20\d{6}").as_("date")
)
async def add_contract_date(
    message: types.Message,
    state: FSMContext,
    date: Match[str]
):
    """Обрабатывает получение даты контракта и сохраняет информацию о ней."""
    await state.update_data(date=date.group(0))
    await state.set_state(RegisterAgency.name)
    return await message.answer(
        "✍ Укажите имя контракта (например, 'Контракт с агентством')."
    )


@add_agency_router.message(
    RegisterAgency.name,
    F.text.regexp(r"[a-zA-Zа-яА-Я0-9\s]+").as_("name")
)
async def add_contract_name(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    name: Match[str]
):
    """Обрабатывает получение имени контракта и сохраняет информацию об агентстве."""
    all_data = await state.get_data()
    all_data["name"] = name.group(0)
    all_data["photographer_id"] = message.from_user.id
    agency, manager, bank_account = await save_agency(session=session, **all_data)

    # Prepare a concise summary of the saved agency
    agency_summary = (
        f"🏢 Компания: {agency.name or 'Неизвестно'}\n"
        f"📍 Адрес: {agency.address or 'Неизвестно'}\n"
        f"👤 Менеджер: {manager.full_name or 'Неизвестно'}\n"
        f"🏦 Банк: {bank_account.name or 'Неизвестно'}\n"
        f"📅 Дата контракта: {all_data.get('date', 'Неизвестно')}\n"
        f"✍ Имя контракта: {all_data.get('name', 'Неизвестно')}"
    )

    await state.clear()
    return await message.answer(
        f"✅ Агентство успешно зарегистрировано!\n\n{agency_summary}\n\n🎉 Регистрация завершена!",
        reply_markup=await start_menu()
    )

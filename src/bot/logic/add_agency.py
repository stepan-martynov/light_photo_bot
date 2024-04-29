from pprint import pprint
from re import Match
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.bot.filters.user_role_filter import UserRoleFilter
from src.bot.logic.ext import print_state_data
from src.bot.structure.kb.main_menu import start_menu
from src.db.models import Agency, Manager, BankAccaunt

from src.api.dadata.api_requests import dadata_connection
from src.db.requests.add_agency import save_agency


class RegisterAgency(StatesGroup):
    inn = State()
    bik = State()
    paymant_account = State()
    contract = State()


add_agency_router = Router()
add_agency_router.message.filter(UserRoleFilter(user_role="photographer"))
add_agency_router.callback_query.filter(UserRoleFilter(user_role="photographer"))



@add_agency_router.callback_query(F.data == "add_agency", StateFilter(None))
async def add_agency(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.set_state(RegisterAgency.inn)
    return await callback.message.answer("Пришлите ИНН")


@add_agency_router.message(
    RegisterAgency.inn,
    F.text.regexp(r"\d{10}").as_("inn"),
)
async def add_agency(message: types.Message, state: FSMContext, inn: Match[str]):
    try:
        agency, manager = dadata_connection.get_company(str(inn.group(0)))
        await state.update_data(agency=agency)
        await state.update_data(manager=manager)
    except:
        return await message.answer("Компания не найдена. Возможно неправильно введен ИНН")
    await state.set_state(RegisterAgency.bik)
    return await message.answer(f"Вы прислали ИНН {str(inn.group(0))}.\
        Мы нашли следующую компанию: {agency}.\nИ менеджера: {manager}.\nПришлите БИК")


@add_agency_router.message(
    RegisterAgency.bik,
    F.text.regexp(r"\d{9}").as_("bik"),
)
async def add_agency_bank(message: types.Message, state: FSMContext, bik: Match[str]):
    try:
        bank = dadata_connection.get_bank_accaunt(str(bik.group(0)))
        await state.update_data(bank=bank)
    except:
        return await message.answer("Банк не найден. Возможно неправильно введен БИК")
    await state.set_state(RegisterAgency.paymant_account)
    return await message.answer(f"Ваш банк {bank}. \nВведите счет для оплаты (20 цифр)")


@add_agency_router.message(
    RegisterAgency.paymant_account,
    F.text.regexp(r"\d{20}").as_("paymant_account")
)
async def add_bank_account(
    message: types.Message,
    state: FSMContext,
    paymant_account: Match[str]
):
    paymant_account = paymant_account.group(0)
    await state.update_data(paymant_account=paymant_account)
    await state.set_state(RegisterAgency.contract)
    return await message.answer(f"Укажите дату заключения контракта в формате ггггммдд.")


@add_agency_router.message(
        RegisterAgency.contract,
        F.text.regexp(r"20\d{6}").as_("date")
)
async def add_contract_date(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    date: Match[str]
):
    all_data = await state.get_data()
    all_data["contract"] = date.group(0)
    photographer_id = message.from_user.id
    all_data["photographer_id"] = photographer_id
    await save_agency(session=session, **all_data)
    msg = await print_state_data("мы сохранили агенство: ", all_data)
    await state.clear()
    return await message.answer(f"{msg}", reply_markup=await start_menu())

import pprint
from re import Match
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.db.models import Agency, Manager, BankAccaunt

from src.bot.structure.fsm.add_agency import RegisterAgency
from src.api.dadata.api_requests import dadata_connection

add_agency_router = Router()


@add_agency_router.callback_query(F.data == "add_agency", StateFilter(None))
async def add_agency(callback: types.CallbackQuery, state: FSMContext):
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
        Мы нашли следующую компанию: {agency}.\
        И менеджера: {manager}.\
        Пришлите БИК")


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
    return await message.answer(f"Ваш банк {bank}. Введите счет для оплаты (20 цифр)")


@add_agency_router.message(
    RegisterAgency.paymant_account,
    F.text.regexp(r"\d{20}").as_("paymant_account")
)
async def add_bank_account(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    paymant_account: Match[str]
):
    # await state.update_data(paymant_account=paymant_account.group(0))
    # all_data = await state.get_data()
    paymant_account=paymant_account.group(0)
    all_data = await state.get_data()
    all_data["agency"]["paymant_account"] = paymant_account
    agency = Agency(**all_data['agency'])
    manager = Manager(**all_data['manager'])
    bank_account = BankAccaunt(**all_data['bank'])
    agency.manager = manager
    agency.bank_accaunt = bank_account
    session.add_all((agency, manager, bank_account))
    await session.commit()
    await state.clear()
    return await message.answer(f"мы сохранили агенство{all_data}")

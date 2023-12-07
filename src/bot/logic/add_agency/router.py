from re import Match
from aiogram.filters import StateFilter
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from ...structure.fsm.add_agency import RegisterAgency

add_agency_router = Router()

# TODO add fsm


@add_agency_router.callback_query(F.data == "add_agency", StateFilter(None))
async def add_agency(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegisterAgency.inn)
    return await callback.message.answer("Пришлите ИНН")


@add_agency_router.message(
    RegisterAgency.inn,
    F.text.regexp(r"\d{10}").as_("inn"),
)
async def add_agency(message: types.Message, state: FSMContext, inn: Match[str]):
    # TODO find agency by inn in dadata
    await state.set_state(RegisterAgency.bik)
    return await message.answer(f"Вы прислали ИНН {str(inn.group(0))}. Пришлите БИК")


@add_agency_router.message(
    RegisterAgency.bik,
    F.text.regexp(r"\d{9}").as_("bik"),
)
async def add_agency(message: types.Message, state: FSMContext, bik: Match[str]):
    await state.clear()
    return await message.answer(f"Неплохо {str(bik.group(0))}.")

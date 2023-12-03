from re import Match
from aiogram import F, Router, types

add_agency_router = Router()

#TODO add fsm

@add_agency_router.message(F.text=="Добавить агентство")
async def add_agency(message: types.Message):
    return await message.answer("Пришлите ИНН")


@add_agency_router.message(F.text.regexp(r"\d{10}").as_("inn"))
async def add_agency(message: types.Message, inn: Match[str]):
    # TODO find agency by inn in dadata
    return await message.answer("Пришлите БИК")


@add_agency_router.message(F.text.regexp(r"\d{9}").as_("bik"))
async def add_agency(message: types.Message, bik: Match[str]):
    return await message.answer(f"Неплохо {bik}")

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.db.models.agency import Agency
from src.db.models.service import Service


async def agencies_kb(agencies: list[Agency]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for agency in agencies:
        kb.button(text=agency.name, callback_data=str(agency.id))
    return kb.as_markup()


async def services_kb(servicies: list[Service]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for service in servicies:
        kb.button(text=service.name, callback_data=service.id)
    return kb.as_markup()

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
        kb.button(text=f'{service.name} {service.default_price}', callback_data=f'{service.id}_{service.default_price}')
    kb.adjust(1)
    return kb.as_markup()


async def check_kb(userdata: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # Add regular buttons
    for key, value in userdata.items():
        if key not in ["img_list", ]:
            kb.button(text=f"{key}", callback_data=f'{key}')
    # Adjust layout: 2 buttons per row for regular buttons, then 1 button row for confirm
    kb.adjust(2)
    # Add confirm button in its own row
    kb.row(InlineKeyboardButton(text="Подтвердить", callback_data="confirm"))
    return kb.as_markup()

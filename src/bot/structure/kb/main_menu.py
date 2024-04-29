from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder



async def start_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.button(text="Добавить агентство", callback_data="add_agency")
    menu.button(text="Добавить фотосессию", callback_data="add_photosession")
    menu.button(text="Добавить услугу", callback_data="add_service")
    return menu.as_markup()


async def role_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.button(text="Фотограф", callback_data="photographer")
    menu.button(text="Брокер", callback_data="broker")
    return menu.as_markup()

async def contact() -> ReplyKeyboardMarkup:
    menu = ReplyKeyboardBuilder()
    menu.button(text="Отправить свои номер", request_contact=True)
    return menu.as_markup(resize_keyboard=True)

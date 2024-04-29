from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

async def kb_generator(buttons: list | tuple, resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for button in buttons:
        kb.add(KeyboardButton(text=button))
    return kb.as_markup(resize_keyboard=resize_keyboard)

async def inline_kb_generator(buttons: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k, v in buttons.items:
        kb.button(text=k, callback_data=v)
    return kb.as_markup()

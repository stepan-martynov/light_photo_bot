from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

async def kb_generator(buttons: list | tuple, resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for button in buttons:
        kb.add(KeyboardButton(text=button))
    return kb.as_markup(resize_keyboard=resize_keyboard)

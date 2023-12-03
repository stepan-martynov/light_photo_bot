from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


START_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить агентство")]
    ], 
    resize_keyboard=True, 
    one_time_keyboard=True
)


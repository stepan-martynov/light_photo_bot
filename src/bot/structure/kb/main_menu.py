from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


START_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить агентство", callback_data="add_agency"
            )
        ],
        [
            InlineKeyboardButton(
                text="Добавить фотосессию", callback_data="add_photosession"
            )
        ]
    ]
)

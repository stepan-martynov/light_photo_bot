from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


START_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить агентство")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

STSRT_MENU = InlineKeyboardMarkup(
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

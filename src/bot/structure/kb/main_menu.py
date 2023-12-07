from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


START_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить агентство")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

ADD_AGENCY_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить агентство", callback_data="add_agency"
            )
        ]
    ]
)

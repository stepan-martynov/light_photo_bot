from aiogram.fsm.state import State, StatesGroup

class RegisterPhotosession(StatesGroup):
    url: State()
    brocker: State()
    location: State()
    price: State()

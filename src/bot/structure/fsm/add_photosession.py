from aiogram.fsm.state import State, StatesGroup

class RegisterPhotosession(StatesGroup):
    url = State()
    date = State()
    agency = State()
    # brocker = State()
    service = State()
    price = State()

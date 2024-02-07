from aiogram.fsm.state import State, StatesGroup

class RegisterPhotosession(StatesGroup):
    url = State()
    agency = State()
    # brocker = State()
    service = State()
    # location = State()
    price = State()

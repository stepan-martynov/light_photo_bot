from aiogram.fsm.state import StatesGroup, State

class RegisterAgency(StatesGroup):
    inn = State()
    bik = State()
    paymant_account = State()
    cor_account = State()
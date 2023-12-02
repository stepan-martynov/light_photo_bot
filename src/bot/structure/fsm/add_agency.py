from aiogram.fsm.state import StateGroup, State

class RegisterAgencyGroup(StateGroup):
    inn = State()
    bik = State()
    paymant_account = State()
    cor_account = State()
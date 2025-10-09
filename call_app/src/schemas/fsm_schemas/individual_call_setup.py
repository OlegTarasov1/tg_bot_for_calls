from aiogram.fsm.state import StatesGroup, State


class IndividualCallState(StatesGroup):
    time_for_call = State()
    verification = State()
    

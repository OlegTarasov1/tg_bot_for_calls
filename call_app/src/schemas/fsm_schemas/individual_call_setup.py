from aiogram.fsm.state import StatesGroup, State


class IndividualCallState(StatesGroup):
    get_data = State()
    validation = State()
    final_check = State()
    
    

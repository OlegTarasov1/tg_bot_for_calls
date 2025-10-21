from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class RescheduleState(StatesGroup):
    user_data = State()
    schedule_time = State()
    reschedule = State()
    schedule_date = State()


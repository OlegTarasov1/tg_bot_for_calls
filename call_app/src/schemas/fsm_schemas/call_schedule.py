from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class ScheduleState(StatesGroup):
    user_data = State()
    schedule_time = State()
    reschedule = State()
    schedule_date = State()


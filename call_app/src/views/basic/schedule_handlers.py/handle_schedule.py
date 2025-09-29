from schemas.fsm_schemas.call_schedule import ScheduleState
from aiogram.fsm.context import FSMContext
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from aiogram.types import Message
from aiogram import Router


schedule_setting_handler = Router()


@schedule_setting_handler.message(ScheduleState.schedule)
async def set_schedule(msg: Message, state: FSMContext):
    schedule = state.get_data()
    await state.clear()

    if schedule == "Утро (8:00)":
        await AsyncRequestsUser.update_user_call_group(
            user_id = msg.from_user.id,
            call_id_to_update = 2
        )
        await msg.answer("Время установлено на 8:00 успешно.")
    elif schedule == "Вечер (18:00)":
        await AsyncRequestsUser.update_user_call_group(
            user_id = msg.from_user.id,
            call_id_to_update = 3
        )
        await msg.answer("Вемя установлено на 18:00 успешно.")
    else:
        await msg.answer("Что-то пошло не так, время не было изменино.")
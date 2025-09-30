from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.kbs_get_menue import get_menu_keyboard
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from pydantic import ValidationError
from utils.keyboards.kb_temp import temp_kb
from aiogram.fsm.context import FSMContext
from schemas.fsm_schemas.call_schedule import ScheduleState
from views.basic.schedule.another_schedule import schedule_setting_handler
import logging


basic_router = Router()

basic_router.include_router(schedule_setting_handler)


@basic_router.message(Command("set_call"))
async def start_handler(
    msg: Message,
    state: FSMContext
):
    user = await AsyncRequestsUser.get_user_by_id(
        id = msg.from_user.id
    )
    await state.set_state(ScheduleState.schedule)

    await msg.answer(
        "К какому созвону вы бы хотели присоединиться?",
        reply_markup = temp_kb
    )

    if not user:
        try:
            user_data = UserTemplate(
                **msg.from_user.model_dump(),
                chat_id = msg.chat.id
            )

            await AsyncRequestsUser.new_user(
                from_user = user_data
            )

        except ValidationError:
            logging.warning("что-то не так с данными: " + msg.from_user)

    else:
        pass


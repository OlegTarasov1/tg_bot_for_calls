from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.kbs_get_menue import get_menu_keyboard
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from pydantic import ValidationError
from .user_callbacks.list_users import list_users_handler
from .user_callbacks.menu_handler import user_menu_router
from .schedule.schedule_router import schedule_router
from tasks.tasks import message_before_call
import logging


basic_router = Router()

basic_router.include_router(list_users_handler)
basic_router.include_router(user_menu_router)
basic_router.include_router(schedule_router)


@basic_router.message(Command("start"))
async def start_handler(msg: Message):
    user = await AsyncRequestsUser.get_user_by_id(
        id = msg.from_user.id
    )
    
    message_before_call.apply_async(
        args = ["some text", 1],
        countdown = 5
    )

    if not user:
        await msg.answer("вас нет в базе")
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
        await msg.answer(
            "Выберите:",
            reply_markup = get_menu_keyboard(
                is_admin = user.is_admin,
                is_scrum = user.is_scrum
            )
        )
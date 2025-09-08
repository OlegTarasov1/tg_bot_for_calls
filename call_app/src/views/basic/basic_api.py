from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.kbs_get_menue import get_menu_keyboard
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from pydantic import ValidationError
from .callback_handlers.list_users import list_users_handler
import logging


basic_router = Router()

basic_router.include_router(list_users_handler)


@basic_router.message(Command("start"))
async def start_handler(msg: Message):
    user = await AsyncRequestsUser.get_user_by_id(
        id = msg.from_user.id
    )

    if not user:
        await msg.answer("вас нет в базе")
        try:
            user_data = UserTemplate(**msg.from_user.model_dump())
            await AsyncRequestsUser.new_user(
                from_user = user_data
            )
        except ValidationError:
            logging.warning("что-то не так с данными: " + msg.from_user)

    else:
        logging.warning(
            f"is_admin: {user.is_admin},\nis_scrum: {user.is_scrum}"
        )
        await msg.answer(
            "Выберите:",
            reply_markup = get_menu_keyboard(
                is_admin = user.is_admin,
                is_scrum = user.scrum
            )
        )
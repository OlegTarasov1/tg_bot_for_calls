from typing import Callable, Awaitable, Any, Dict
from aiogram.types import Message
from aiogram import BaseMiddleware
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from schemas.user_pydantic_schemas.user_schema import UserTemplate
import logging
import os


class AuthorizationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_data = await AsyncRequestsUser.get_user_by_id(event.from_user.id)
        
        if not user_data:
            user_data = UserTemplate(
                **event.from_user.model_dump(),
                chat_id = event.chat.id
            )

            user_data = await AsyncRequestsUser.new_user(
                from_user = user_data
            )
            logging.warning(user_data)

        if user_data.is_an_employee:
            return await handler(event, data)

        elif not user_data.is_an_employee and event.text.strip() == os.getenv("ENTER_PASSWORD"):
                await event.answer("пароль верный, вы отмечены как сотрудник")

                await AsyncRequestsUser.new_employee(
                    user_id = event.from_user.id
                )
        else:
            await event.answer("Введите пароль, чтобы вас добавили в базу.")
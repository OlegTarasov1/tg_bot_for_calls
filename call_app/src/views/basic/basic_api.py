from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.meta_kbs import get_menu_keyboard

basic_router = Router()


@basic_router.message(Command("start"))
async def start_handler(msg: Message):
    user = await AsyncRequestsUser.new_user(msg.from_user)

    if not user:
        await msg.answer("отправлен запрос на добавление в бд")
    else:
        await msg.answer(
            "Выберите:",
            reply_markup= await get_menu_keyboard(
                is_admin = user.is_admin,
                is_scrum = user.scrum
            )
        )
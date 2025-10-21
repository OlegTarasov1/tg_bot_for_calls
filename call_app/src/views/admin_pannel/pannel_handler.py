from utils.async_sql_requests.user_requests import AsyncRequestsUser
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from views.admin_pannel.handle_callbacks.retreive_calls import cb_calls_retreival_router
from utils.keyboards.menu_kb.employee_kb import employee_menu
from utils.keyboards.menu_kb.admin_kb import admin_menu
from views.admin_pannel.individual_calls.individual_calls_declare import individual_call_handler


admin_pannel_router = Router()
admin_pannel_router.include_router(cb_calls_retreival_router)
admin_pannel_router.include_router(individual_call_handler)


@admin_pannel_router.message(Command("start"))
async def get_command_pannel(
    msg: Message
):
    user_data = await AsyncRequestsUser.get_user_by_id(
        id = msg.from_user.id
    )
    if user_data.is_admin:
        await msg.answer(
            "Админ панель:",
            reply_markup = employee_menu
        )
    elif user_data.is_an_employee:
        await msg.answer(
            "Панель пользователя:",
            reply_markup = employee_menu
        )
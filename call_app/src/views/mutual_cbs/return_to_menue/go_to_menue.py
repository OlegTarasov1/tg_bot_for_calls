from utils.keyboards.menu_kb.employee_kb import employee_menu
from utils.keyboards.menu_kb.admin_kb import admin_menu
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from aiogram.types import CallbackQuery
from aiogram import Router, F


back_to_menue_router = Router()


@back_to_menue_router.callback_query(F.data == "menu")
async def return_menue(
    query: CallbackQuery
):
    user = await AsyncRequestsUser.get_user_by_id(
        id = query.from_user.id
    )
    
    if user.is_admin:
        await query.message.edit_text(
            text = "Меню",
            reply_markup = admin_menu
        )
    else:
        await query.message.edit_text(
            text = "Меню",
            reply_markup = employee_menu
        )
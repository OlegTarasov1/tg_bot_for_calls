from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.keyboards.menu_kb.employee_kb import employee_menu
from aiogram.types import CallbackQuery
from aiogram import Router, F

delete_call_user_connection_router = Router()


@delete_call_user_connection_router.callback_query(RetreiveCallCB.filter(F.action == "delete"))
async def delete_call(
    query: CallbackQuery,
    callback_data: RetreiveCallCB
):
    await AsyncCallRequets.delete_user_call_connection(
        user_id = callback_data.user_id,
        call_id = callback_data.call_id
    )

    await query.message.edit_text(
        text = "Вы отписались от созвона успешно.",
        reply_markup = employee_menu
    )
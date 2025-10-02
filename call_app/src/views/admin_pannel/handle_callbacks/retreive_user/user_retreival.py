from views.admin_pannel.handle_callbacks.retreive_user.selected_call.delete_call import delete_call_user_connection_router
from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from utils.keyboards.menu_kb.expended_user_kb import get_user_expended_kb
from utils.async_sql_requests.call_requests import AsyncCallRequets
from aiogram.types import CallbackQuery
from aiogram import Router, F


expand_user_router = Router()
expand_user_router.include_router(delete_call_user_connection_router)

@expand_user_router.callback_query(RetreiveCallCB.filter(F.action == "retreive_more"))
async def more_on_user(
    query: CallbackQuery,
    callback_data: RetreiveCallCB
):
    call_data = await AsyncCallRequets.retreive_call(
        call_id = callback_data.call_id
    ) 
    await query.message.edit_text(
        text = f"Запланированный созвон на: {call_data.time.strftime('%H:%M')}",
        reply_markup = await get_user_expended_kb(
            user_id = callback_data.user_id,
            call_id = callback_data.call_id
        )
    )

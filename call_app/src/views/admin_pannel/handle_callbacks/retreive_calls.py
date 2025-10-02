from schemas.cb_schemas.menu_schemas.get_calls_schema import CallsCB
from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.keyboards.menu_kb.list_calls_kb import list_calls_for_user
from views.admin_pannel.handle_callbacks.retreive_user.user_retreival import expand_user_router

cb_calls_retreival_router = Router()
cb_calls_retreival_router.include_router(expand_user_router)


@cb_calls_retreival_router.callback_query(CallsCB.filter())
async def return_scheduled_calls(
    query: CallbackQuery,
    callback_data: CallsCB
):
    calls = await AsyncCallRequets.get_calls_for_user(
        id = query.from_user.id
    )

    await query.message.edit_reply_markup(
        text = "запланированные созвоны:",
        reply_markup = await list_calls_for_user(
            calls = calls,
            page = callback_data.page,
            is_admin = calls.is_admin
        )
    )






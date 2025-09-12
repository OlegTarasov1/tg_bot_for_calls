from schemas.cb_schemas.call_cb_schema import RetreiveCallsCallBack
from utils.async_sql_requests.call_requests import AsyncCallRequets
from utils.keyboards.kb_calls import list_calls
from aiogram.types import CallbackQuery
from aiogram import Router, F


schedule_router = Router()


@schedule_router.callback_query(RetreiveCallsCallBack.filter(F.action == "user"))
async def get_schedule(
    query: CallbackQuery,
    callback_data: RetreiveCallsCallBack
):
    calls = await AsyncCallRequets.get_calls_for_user(id = query.from_user.id)

    all_calls = calls.calls_employees
    all_calls.extend(calls.calls_scrum_masters)

    await query.message.edit_text(
        text = "созвоны:",
        reply_markup = await list_calls(
            user_data = all_calls
        )
    )
from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from aiogram.types import CallbackQuery
from aiogram import Router, F


expand_user_router = Router()


@expand_user_router.callback_query(RetreiveCallCB.filter())
async def more_on_user(
    query: CallbackQuery,
    callback_data: RetreiveCallCB
):
    
    await query.message.edit_text(
        text = "",
        reply_markup = ...
    )

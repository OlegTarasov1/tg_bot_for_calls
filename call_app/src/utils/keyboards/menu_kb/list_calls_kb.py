from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from schemas.cb_schemas.menu_schemas.get_calls_schema import CallsCB
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardButton
from models.models import UsersBase


async def list_calls_for_user(
    calls: UsersBase,
    page: int,
    page_limit: int = 6,
    is_admin: bool = False
):
    page -= 1
    kb = InlineKeyboardBuilder()
    
    for i in calls.calls[page * page_limit, page * page_limit + page_limit]:
        kb.add(
            InlineKeyboardButton(
                text = f"{i.time.strftime("%H:%M")} | {i.call_purpose}",
                callback_data = RetreiveCallCB(
                    action = "retreive_more",
                    user_id = calls.id,
                    call_id = i.id
                ).pack()
            )
        )

    if page >= 1:
        kb.add(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = CallsCB(
                    page = page - 1
                ).pack()
            )
        ) 
    if len(calls.calls) - ( page * page_limit + page_limit) > 0:
        kb.add(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = CallsCB(
                    page = page + 1
                ).pack()
            )
        )
    kb.add(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.adjust(1).as_markup()

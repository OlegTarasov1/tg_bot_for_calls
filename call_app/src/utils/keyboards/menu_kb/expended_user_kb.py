from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardButton


async def get_user_expended_kb(
    user_id: int,
    call_id: int
):
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text = "Отписаться от созвона",
            callback_data = RetreiveCallCB(
                action = "delete",
                user_id = user_id,
                call_id = call_id 
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Перенести",
            callback_data = "shutter"
        ),
        InlineKeyboardButton(
            text = "Вернуться в меню",
            callback_data = "shutter"
        )
    )

    return kb.adjust(1).as_markup()
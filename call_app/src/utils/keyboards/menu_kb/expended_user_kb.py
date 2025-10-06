from schemas.cb_schemas.menu_schemas.retreive_call_schema import RetreiveCallCB
from utils.keyboards.menu_kb.employee_kb import employee_menu
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
            callback_data = RetreiveCallCB(
                action = "reschedule",
                user_id = user_id,
                call_id = call_id 
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Вернуться в меню",
            callback_data = "menu"
        )
    )

    return kb.adjust(1).as_markup()
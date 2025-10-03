from schemas.cb_schemas.menu_schemas.get_calls_schema import CallsCB
from aiogram.types import InlineKeyboardButton


async def go_back_to_menue(
    is_admin: bool
) -> InlineKeyboardButton:
    if is_admin:
        return InlineKeyboardButton(
            text = "Посмотреть назначенные созвоны",
            callback_data = CallsCB(page = 1).pack()
        )
    else:
        return None
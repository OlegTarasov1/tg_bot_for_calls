from schemas.cb_schemas.menu_schemas.get_calls_schema import CallsCB
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "Посмотреть назначенные созвоны",
                callback_data = CallsCB(page = 1).pack()
            )
        ]
    ]
)


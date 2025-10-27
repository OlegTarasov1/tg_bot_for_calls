from schemas.cb_schemas.menu_schemas.get_calls_schema import CallsCB
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "Отпарвить приглашения массово",
                callback_data = "start_mass_invitng"
            )
        ],
        [
            InlineKeyboardButton(
                text = "Посмотреть назначенные созвоны",
                callback_data = CallsCB(
                    func = "calls",
                    page = 1
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text = "Установить новый созвон",
                callback_data = "setup_new_call"
            )
        ],
        [
            InlineKeyboardButton(
                text = "Установить индивидуальный созвон",
                callback_data = "shutter"
            )
        ]
    ]
)


from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


temp_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "Утро (8:00)"),
            KeyboardButton(text = "Вечер (18:00)")
        ]
    ],
    resize_keyboard = True
)


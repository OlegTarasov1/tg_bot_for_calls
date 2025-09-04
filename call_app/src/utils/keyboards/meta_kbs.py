from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


# Меню клавиатура
def get_menu_keyboard(is_admin: bool = False, is_scrum: bool = False):
    buttons = [
        [InlineKeyboardButton("\U0001f4c5 Расписание", callback_data="call_page_1")],
    ]

    if is_admin or is_scrum:
        buttons.append(
            [
                InlineKeyboardButton(
                    "\U0001f4d6 Список сотрудников", callback_data="users_page_1"
                )
            ]
        )
        buttons.append(
            [InlineKeyboardButton("\U0001f6b7 Пропуски", callback_data="missed_call")]
        )
    if is_scrum:
        buttons.append(
            [
                InlineKeyboardButton(
                    "\U0001f504 Обновить ссылку", callback_data="update_call_link"
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                "\U0000274c Больше не работаю", callback_data="dont_work"
            )
        ]
    )
    inline_keyboard = InlineKeyboardMarkup(buttons)

    return inline_keyboard

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from schemas.cb_schemas.list_users_schema import ListUsersCallBack


def get_menu_keyboard(is_admin: bool = False, is_scrum: bool = False, page: int = 0) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="\U0001f4c5 Расписание", callback_data="call_page_1")],
    ]

    if is_admin:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text = "\U0001f4d6 Список сотрудников",
                    callback_data =  ListUsersCallBack(
                        page = page
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(text="\U0001f6b7 Пропуски", callback_data="missed_call")
            ],
        ])

    if is_scrum:
        buttons.extend([
            [InlineKeyboardButton(text="\U0001f504 Обновить ссылку", callback_data="update_call_link")],
        ])

    buttons.append([
        InlineKeyboardButton(text="\U0000274c Больше не работаю", callback_data="dont_work")
    ])

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


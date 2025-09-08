from schemas.cb_schemas.retreive_user_callback import RetreiveUserCallBack
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models.models import UserBase

# Список сотрудников
def create_user_list_keyboard(
    employees: list[UserBase],
    page: int,
    employees_per_page: int,
    is_admin: bool = False
) -> InlineKeyboardMarkup:

    page_buttons = [
        [
            InlineKeyboardButton(
                f"{employee.first_name} {employee.last_name}",
                callback_data=RetreiveUserCallBack(id = employee.id).pack()
            )
        ]
        for employee in employees
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                "\U000025c0 Назад", callback_data=f"users_page_{page - 1}"
            )
        )

    nav_buttons.append(InlineKeyboardButton("\U0001f4d2 Меню", callback_data="menu"))

    if employees_per_page == len(employees):
        nav_buttons.append(
            InlineKeyboardButton(
                "\U000025b6 Вперед", callback_data=f"users_page_{page + 1}"
            )
        )

    page_buttons.append(nav_buttons)
    if is_admin:
        page_buttons.append(
            [
                InlineKeyboardButton(
                    "\U00002795 Добавить сотрудника", callback_data="add_employee"
                )
            ]
        )

    inline_keyboard = InlineKeyboardMarkup(page_buttons)
    return inline_keyboard
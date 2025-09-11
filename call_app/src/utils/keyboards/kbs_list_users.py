from schemas.cb_schemas.retreive_user_callback import RetreiveUserCallBack
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from schemas.cb_schemas.list_users_schema import ListUsersCallBack
from models.models import UserBase
from aiogram.utils.keyboard import InlineKeyboardBuilder





async def create_user_list_keyboard(
    employees: list[UserBase],
    page: int,
    employees_per_page: int,
    is_admin: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i in employees:
        builder.add(
            InlineKeyboardButton(
                text = f"{i.first_name} {i.last_name}",
                callback_data = RetreiveUserCallBack(id = i.id).pack()
            )
        )
    if page > 0:
        builder.add(
            InlineKeyboardButton(
                "\U000025c0 Назад",
                callback_data = ListUsersCallBack(page = page - 1).pack()
            )
        )

    if employees_per_page == len(employees):
        builder.add(
            InlineKeyboardButton(
                text = "\U000025b6 Вперед",
                callback_data = ListUsersCallBack(page = page + 1).pack()
            )
        )

    if is_admin:
        builder.add(
            InlineKeyboardButton(
                text = "\U00002795 Добавить сотрудника",
                callback_data="add_employee"
            )
        )

    return builder.adjust(1).as_markup()


from schemas.cb_schemas.admin_schemas.list_users_schema import UsersCB
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardButton
from models.models import UsersBase


async def get_user_expended_kb(
    page_offset: int,
    are_more_pages: bool,
    users: list[UsersBase]
):

    kb = InlineKeyboardBuilder()

    kb.add(
        *[
            InlineKeyboardButton(
                text = f"{i.username} | {i.first_name} | {i.last_name}",
                callback_data = UsersCB(
                    function = "mass_invite",
                    user_id = i.id,
                    chat_id = i.chat_id,
                    username = i.username
                ).pack()
            ) for i in users
        ]
    )    

    if page_offset > 0:
        kb.add(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = UsersCB(
                    function = "mass_invite_new_page",
                    page_offset = page_offset - 1 
                )
            )
        )
    if are_more_pages:
        kb.add(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = UsersCB(
                    function = "mass_invite_new_page",
                    page_offset = page_offset + 1
                )
            )
        )   

    return kb.adjust(1).as_markup()
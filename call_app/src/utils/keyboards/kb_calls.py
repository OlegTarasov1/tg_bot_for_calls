from aiogram.utils.keyboard import InlineKeyboardBuilder 
from models.models import UserBase, CallsBase

from schemas.cb_schemas.retreive_user_callback import RetreiveUserCallBack
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from schemas.cb_schemas.list_users_schema import ListUsersCallBack
from models.models import UserBase
from aiogram.utils.keyboard import InlineKeyboardBuilder



async def list_calls(
    user_data: list[CallsBase],
    page: int = 0,
    data_per_page: int = 6
) -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()

    page_start = page * data_per_page
    page_end = page_start + data_per_page

    for i in user_data[page_start:page_end]:
        kb.add(
            InlineKeyboardButton(
                text = f"{i.time.strftime('%d.%m %H:%M')} | {i.call_purpouse}"
            )
        )

    kb.add(
        InlineKeyboardButton(
            text = "\U0001f4c5 меню",
            callback_data = "menu"
        )
    )

    return kb.adjust(1).as_markup()
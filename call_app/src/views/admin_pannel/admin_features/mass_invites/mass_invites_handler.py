from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.admin_kb.list_users_kb import get_user_expended_kb
from schemas.cb_schemas.admin_schemas.list_users_schema import UsersCB
from utils.extra_funcs.send_message import send_message
from schemas.raw_templates.template_call import get_call_text_template
from datetime import datetime

mass_invites_router = Router()


@mass_invites_router.callback_query(F.data == "start_mass_invitng")
async def list_users_to_send(
    callback_query: CallbackQuery
):
    users = await AsyncRequestsUser.list_users(
        page_offset=0
    )
    are_more_pages = await AsyncRequestsUser.list_users(
        page_offset=1
    )
    await callback_query.message.edit_text(
        text = "выберите пользователей, которым отправить сообщение",
        reply_markup = await get_user_expended_kb(
            users = users,
            page_offset = 0,
            are_more_pages = bool(len(are_more_pages))
        )
    )


@mass_invites_router.callback_query(UsersCB.filter(F.function == "mass_invite"))
async def send_invite_to_user(
    callback_query: CallbackQuery,
    callback_data: UsersCB
):
    await callback_query.answer("Сообщение отправлено: ")
    await send_message(
        chat_id = callback_data.chat_id,
        message = get_call_text_template(datetime.now().time())
    )


@mass_invites_router.callback_query(UsersCB.filter(F.function == "mass_invite_new_page"))
async def switch_page(
    callback_query: CallbackQuery,
    callback_data: UsersCB
):
    users = await AsyncRequestsUser.list_users(
        page_offset = callback_data.page_offset
    )
    are_more_pages = await AsyncRequestsUser.list_users(
        page_offset = callback_data.page_offset + 1
    )

    await callback_query.message.edit_text(
        text = "выберите пользователей, которым отправить сообщение",
        reply_markup = await get_user_expended_kb(
            users = users,
            page_offset = callback_data.page_offset,
            are_more_pages = bool(len(are_more_pages))
        )
    )
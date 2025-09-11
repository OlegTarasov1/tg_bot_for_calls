from schemas.cb_schemas.list_users_schema import ListUsersCallBack
from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.kbs_list_users import create_user_list_keyboard
from schemas.cb_schemas.retreive_user_callback import RetreiveUserCallBack
from utils.keyboards.kbs_get_menue import menu

list_users_handler = Router()



@list_users_handler.callback_query(ListUsersCallBack.filter(F.action == "test"))
async def list_users(
    query: CallbackQuery,
    callback_data: ListUsersCallBack
):

    user = await AsyncRequestsUser.get_user_by_id(
        id = query.from_user.id
    )

    list_users = await AsyncRequestsUser.list_users(
        page_offset = callback_data.page
    )
    await query.message.edit_reply_markup(
        reply_markup = await create_user_list_keyboard(
            employees = list_users,
            is_admin = user.is_admin,
            employees_per_page = 6,
            page = 0
        )
    )

@list_users_handler.callback_query(RetreiveUserCallBack.filter(F.action == "user_info"))
async def get_user_info(
    query: CallbackQuery,
    callback_data: RetreiveUserCallBack
):
    caller_data = await AsyncRequestsUser.get_user_by_id(id = query.from_user.id)
    user_data = await AsyncRequestsUser.get_user_by_id(id = callback_data.id)

    msg = f"ФИ: {user_data.first_name} {user_data.last_name}\n"
    msg += f"id: {user_data.id}\nпозиция: {user_data.job_title}\n"

    if caller_data.is_admin:
        msg += f"\nадмин: {user_data.is_admin}"

    await query.message.edit_text(
        text=msg,
        reply_markup = menu
    )


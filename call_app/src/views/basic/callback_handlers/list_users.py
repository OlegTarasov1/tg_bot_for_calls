from schemas.cb_schemas.list_users_schema import ListUsersCallBack
from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.kbs_list_users import create_user_list_keyboard

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
        create_user_list_keyboard(
            employees = list_users,
            is_admin = user.is_admin,
            employees_per_page = 6,
            page = 0
        )
    )
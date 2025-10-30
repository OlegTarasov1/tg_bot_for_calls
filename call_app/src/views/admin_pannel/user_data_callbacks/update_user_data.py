from schemas.raw_templates.template_user_data import get_user_data_text
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from aiogram.types import CallbackQuery
from aiogram import Router, F

update_user_data_router = Router()


@update_user_data_router.callback_query(F.data == "get_user_metadata")
async def return_user_data(
    query: CallbackQuery
):
    user_data = await AsyncRequestsUser.get_user_by_id(query.from_user.id)
    await query.message.edit_text(
        text = get_user_data_text(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_admin=user_data.is_admin
        )
    )
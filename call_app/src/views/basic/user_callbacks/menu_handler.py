from schemas.cb_schemas.retreive_user_callback import RetreiveUserCallBack
from utils.async_sql_requests.user_requests import AsyncRequestsUser
from utils.keyboards.kbs_get_menue import menu
from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.keyboards.kbs_get_menue import get_menu_keyboard

user_menu_router = Router()


@user_menu_router.callback_query(F.data == "menu")
async def get_menu(
    cb: CallbackQuery
):
    user_data = await AsyncRequestsUser.get_user_by_id(id = cb.from_user.id)
    await cb.message.edit_text(
        text = "выберите: ",
        reply_markup = get_menu_keyboard(
            is_admin = user_data.is_admin,
            is_scrum = user_data.scrum
        )
    )
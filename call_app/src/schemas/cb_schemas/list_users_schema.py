from aiogram.filters.callback_data import CallbackData


class ListUsersCallBack(CallbackData, prefix = "users_page_"):
    action: str = "test"
    page: int = 0
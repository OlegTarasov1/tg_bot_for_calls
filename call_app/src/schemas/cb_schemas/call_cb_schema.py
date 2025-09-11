from aiogram.filters.callback_data import CallbackData


class RetreiveCallsCallBack(CallbackData, prefix = "get_call_"):
    action: str = "user"
    page: int = 0
    amnt_of_values_by_page: int = 6
    user_id: int = 0
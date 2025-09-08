from aiogram.filters.callback_data import CallbackData


class RetreiveUserCallBack(CallbackData, prefix = "user_info"):
    
    id: int
    last_name: str
    first_name: str
from aiogram.filters.callback_data import CallbackData


class RetreiveUserCallBack(CallbackData, prefix = "user_info_"):
    
    action: str = "user_info"
    id: int

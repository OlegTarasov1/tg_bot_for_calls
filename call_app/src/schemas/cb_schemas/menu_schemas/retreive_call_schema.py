from aiogram.filters.callback_data import CallbackData
from pydantic import Field

class RetreiveCallCB(
    CallbackData,
    prefix = "retreive_call"
):
    action: str
    user_id: int = Field(ge = 1)
    call_id: int = Field(ge = 1)


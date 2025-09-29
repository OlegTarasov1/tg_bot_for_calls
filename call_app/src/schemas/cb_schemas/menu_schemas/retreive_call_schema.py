from aiogram.filters.callback_data import CallbackData
from pydantic import Field

class RetreiveCallCB(
    CallbackData,
    prefix = "retreive_call",
    sep = "!!"
):
    func: str = "call_retreival"
    user_id: int = Field(ge = 1)
    call_id: int = Field(ge = 1)


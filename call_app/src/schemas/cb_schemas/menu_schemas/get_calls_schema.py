from aiogram.filters.callback_data import CallbackData
from pydantic import Field

class CallsCB(
    CallbackData,
    prefix = "menu_calls",
    sep="!!"
):
    func: str = "calls"
    page: int = Field(ge = 1)
    
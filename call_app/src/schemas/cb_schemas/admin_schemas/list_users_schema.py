from aiogram.filters.callback_data import CallbackData
from pydantic import Field

class UsersCB(
    CallbackData,
    prefix = "user_data"
    # sep="!!"
):
    function: str
    
    user_id: int | None = None
    username: str | None = None
    chat_id: int | None = None

    page_offset: int | None = None

    # func: str = "calls"
    # page: int = Field(ge = 1)
    
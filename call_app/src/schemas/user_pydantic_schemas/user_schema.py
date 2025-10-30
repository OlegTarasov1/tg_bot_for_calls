from pydantic import (
    BaseModel,
    Field
)
from aiogram.types import User 


class UserTemplate(
    BaseModel
):
    id: int
    first_name: str | None = Field(max_length=255)
    last_name: str | None = Field(max_length=255)
    username: str = Field(max_length=255)
    chat_id: int

    class Config:
        extra = "ignore"
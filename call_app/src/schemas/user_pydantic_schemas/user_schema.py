from pydantic import (
    BaseModel,
    Field
)
from aiogram.types import User 


class UserTemplate(
    BaseModel
):
    id: int
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    username: str = Field(max_length=255)

    class Config:
        extra = "ignore"
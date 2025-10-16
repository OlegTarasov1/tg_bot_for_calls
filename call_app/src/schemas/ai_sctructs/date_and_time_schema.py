from pydantic import BaseModel, Field, field_validator
from datetime import time, date, datetime
from zoneinfo import ZoneInfo


class DateAndTimeSchema(BaseModel):
    call_time: time | None = None
    call_date: date | None = None
    call_link: str | None = None
    call_purpose: str | None = None
    user_data: str | None = None
    
    
    @field_validator("user_data", mode = "before")
    def validate_user_data(cls, v):
        return cls.validate_none(v)
    
    @field_validator("call_link", mode = "before")
    def validate_call_link(cls, v):
        return cls.validate_none(v)

    @field_validator("call_purpose", mode = "before")
    def validate_call_purpose(cls, v):
        return cls.validate_none(v)

    @field_validator("call_date", mode = "before")
    def validate_call_date(cls, v):
        return cls.validate_none(v)

    @field_validator("call_time", mode = "before")
    def validate_call_time(cls, v):
        return cls.validate_none(v)


    @classmethod
    def validate_none(cls, value):
        if isinstance(value, str):
            if value.lower() == "none":
                return None

        return value


    @field_validator("call_date", mode = "after")
    def set_default_date(cls, v) -> date:
        if not v:
            return datetime.now(ZoneInfo("Europe/Moscow")).date()
        else:
            return v
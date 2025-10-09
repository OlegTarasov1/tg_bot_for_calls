from sqlalchemy.orm import (
    mapped_column,
    Mapped
)
from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
    Time,
    or_
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class UsersBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key = True)
    chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable = True, default = None)

    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255)) 

    is_admin: Mapped[bool] = mapped_column(default = False)
    is_an_employee: Mapped[bool] = mapped_column(default = False)

    calls: Mapped[list["CallsBase"]] = relationship(
        back_populates = "employees",
        secondary = "users_calls_association",
        viewonly = True
    )


class CallsBase(Base):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(primary_key = True)
    master_name: Mapped[str] = mapped_column(String(255)) 
    call_link: Mapped[str] = mapped_column(String(255)) 
    call_purpose: Mapped[str] = mapped_column(String(255)) 
    time: Mapped[datetime | None] = mapped_column(Time, nullable = False)

    employees: Mapped[list["UsersBase"]] = relationship(
        back_populates = "calls",
        secondary = "users_calls_association",
        viewonly = True
    )


class UsersCallsAssociation(Base):
    __tablename__ = "users_calls_association"

    id: Mapped[int] = mapped_column(primary_key = True)

    call_id: Mapped[int] = mapped_column(ForeignKey("calls.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    time: Mapped[datetime | None] = mapped_column(Time, nullable = True) 
    task_id: Mapped[str | None] = mapped_column(nullable = True)
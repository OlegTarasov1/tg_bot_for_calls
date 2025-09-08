from sqlalchemy.orm import (
    mapped_column,
    Mapped
)
from sqlalchemy import (
    BigInteger,
    String
)
from .base import Base


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key = True)

    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255)) 

    is_admin: Mapped[bool] = mapped_column(default = False)
    is_scrum: Mapped[bool | None] = mapped_column(default = False)
    is_employee: Mapped[bool] = mapped_column(default = False)
    scrum: Mapped[bool | None] = mapped_column(nullable=True, default = False)


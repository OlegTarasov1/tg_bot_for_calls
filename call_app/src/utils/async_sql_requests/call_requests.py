from utils.useful.sql_sessions import (
    get_db,
    async_session
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.models import UserBase


class AsyncCallRequets:
    @staticmethod
    async def get_calls_for_user(id: int):
        async with async_session() as session:
            stmt = (
                select(
                    UserBase
                )
                .where(
                    UserBase.id == id
                )
                .options(
                    joinedload(
                        UserBase.calls_scrum_masters
                    ),
                    joinedload(
                        UserBase.calls_employees
                    )
                )
            )

            data = await session.execute(stmt)
            
            return data
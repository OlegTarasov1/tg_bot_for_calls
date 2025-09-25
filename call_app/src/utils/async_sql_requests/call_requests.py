from utils.useful.sql_sessions import (
    get_db,
    async_session
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.models import UsersBase, CallsBase


class AsyncCallRequets:
    @staticmethod
    async def get_calls_for_user(id: int) -> UsersBase:
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.id == id
                )
                .options(
                    selectinload(
                        UsersBase.calls
                    )
                )
            )

            user_calls = await session.execute(stmt)
            user_calls = user_calls.scalar_one_or_none()

            return user_calls
        
    @staticmethod
    async def get_users_for_call(call_id: int) -> CallsBase:
        async with async_session() as session:
            stmt = (
                select(
                    CallsBase
                )
                .where(
                    CallsBase.id == call_id
                )
                .options(
                    selectinload(
                        CallsBase.employees
                    )
                )
            )

            users_for_the_call = await session.execute(stmt)

            users_for_the_call = users_for_the_call.scalar_one_or_none()
            # employees = None
            
            # if users_for_the_call:
            #     employees = users_for_the_call.employees

            return users_for_the_call




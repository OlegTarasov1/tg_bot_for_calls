import logging
from utils.useful.sql_sessions import (
    get_db,
    async_session
)
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import selectinload
from models.models import UsersBase, CallsBase, UsersCallsAssociation


class AsyncCallRequets:
    @staticmethod
    async def delete_user_call_connection(
        user_id: int,
        call_id: int
    ) -> None:
        async with async_session() as session:
            stmt = (
                delete(
                    UsersCallsAssociation
                )
                .where(
                    UsersCallsAssociation.call_id == call_id,
                    UsersCallsAssociation.user_id == user_id
                )
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def retreive_call(
        call_id: int
    ) -> CallsBase:
        async with async_session() as session:
            stmt = (
                select(
                    CallsBase
                )
                .where(
                    CallsBase.id == call_id
                )
            )
            call = await session.execute(stmt)
            call = call.scalar_one_or_none()

            return call

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

            return users_for_the_call

    @staticmethod
    async def delete_call_by_ids(
        user_id: int,
        call_id: int
    ):
        logging.warning(user_id)
        async with async_session() as session:
            stmt = (
                delete(
                    UsersCallsAssociation
                )
                .where(
                    and_(
                        UsersCallsAssociation.user_id == user_id,
                        UsersCallsAssociation.call_id == call_id
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()


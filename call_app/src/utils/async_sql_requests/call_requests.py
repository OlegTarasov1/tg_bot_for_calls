import logging
from utils.useful.sql_sessions import (
    get_db,
    async_session
)
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import selectinload
from models.models import UsersBase, CallsBase, UsersCallsAssociation
from datetime import datetime


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
    async def get_users_for_call(
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
    async def delete_call_by_id(
        id: int
    ) -> None:
        async with async_session() as session:
            stmt = (
                delete(
                    CallsBase
                )
                .where(
                    CallsBase.id == id
                )
            )
            await session.execute(stmt)
            await session.commit()


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


    @staticmethod
    async def add_call(
        call_invoke_id: str,
        master_name: int | None,
        call_link: str | None,
        call_purpose: str | None,
        time: datetime | None,
        days_of_the_week: list[str] | None
    ) -> CallsBase:
        async with async_session() as session:
            new_call = CallsBase(
                master_name = master_name,
                call_link = call_link,
                call_invoke_id = call_invoke_id,
                call_purpose = call_purpose,
                time = time,
                days_of_the_week = days_of_the_week
            )
            session.add(new_call)
            await session.commit()
            
            await session.refresh(new_call)

            return new_call


    @staticmethod
    async def get_todays_calls(
        week_date: int
    ) -> list[CallsBase]:
        async with async_session() as session:
            stmt = (
                select(
                    CallsBase
                )
                .options(
                    selectinload(
                        CallsBase.employees
                    )
                )
                .where(
                    CallsBase.days_of_the_week.contains([week_date])
                )
            )
            calls = await session.execute(stmt)
            calls = calls.unique().scalars().all()

            return calls
            




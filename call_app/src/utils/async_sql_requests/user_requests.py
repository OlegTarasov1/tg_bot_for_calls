from sqlalchemy import select, func, text, desc
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from models.models import UsersBase, UsersCallsAssociation
from sqlalchemy import select, insert, update
from sqlalchemy.orm import joinedload
from utils.useful.sql_sessions import (
    get_db,
    async_session
)
import logging
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from aiogram.types import User


class AsyncRequestsUser:

    @staticmethod
    async def get_user_by_id(
        id: int
    ) -> UsersBase:
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.id == id
                )
            )

            user = await session.execute(stmt)
            user = user.scalar_one_or_none()
            
            if user:
                return user
            else:
                return None
            
            
    @staticmethod
    async def new_user(
        from_user: UserTemplate
    ) -> UsersBase | None:
        async with async_session() as session:

            new_user = UsersBase(
                **from_user.model_dump()
            )

            session.add(new_user)
            await session.commit()

            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.id == from_user.id
                )
            )
            
            user_again = await session.execute(stmt)
            user_again = user_again.scalar_one_or_none()

            return user_again
        

    @staticmethod
    async def list_users(
        page_size: int = 6,
        page_offset: int = 0
    ) -> list[UsersBase]:
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .limit(page_size)
                .offset(page_offset * page_size)
                .order_by(
                    UsersBase.id
                )
            )

            users = await session.execute(stmt)
            users = users.scalars().all()

            return users
        

    @staticmethod
    async def update_user_call_group(
        call_id_to_update: int,
        user_id: int
    ) -> None:
        logging.warning(call_id_to_update)
        async with async_session() as session:
            stmt = (
                select(
                    UsersCallsAssociation
                )
                .where(
                    UsersCallsAssociation.call_id == call_id_to_update,
                    UsersCallsAssociation.user_id == user_id
                )
            )

            is_existent = await session.execute(stmt)
            is_existent = is_existent.scalar_one_or_none()

            if not is_existent:
                stmt = (
                    insert(
                        UsersCallsAssociation
                    )
                    .values(
                        call_id = call_id_to_update,
                        user_id = user_id
                    )
                )

                await session.execute(stmt)
                await session.commit()


    @staticmethod
    async def new_employee(user_id: int) -> None:
        async with async_session() as session:
            stmt = (
                update(
                    UsersBase
                )
                .values(
                    is_an_employee = True
                )
                .where(
                    UsersBase.id == user_id
                )
            )
            
            await session.execute(stmt)
            await session.commit()


    # @staticmethod
    # async def get_user_by_creds(
    #     user_creds: str
    # ) -> UsersBase:
    #     async with async_session() as session:
    #         tsvector = func.to_tsvector(
    #             "russian",
    #             (
    #                 UsersBase.first_name + " " +
    #                 UsersBase.last_name + " " +
    #                 func.coalesce(UsersBase.username, "") + " " +
    #                 func.coalesce(UsersBase.job_title, "")
    #             )
    #         )

    #         tsquery = func.plainto_tsquery("simple", user_creds)

    #         rank = func.ts_rank(tsvector, tsquery)

    #         stmt = (
    #             select(UsersBase, rank.label("rank"))
    #             .where(tsvector.op("@@")(tsquery))
    #             .order_by(desc(rank))
    #             .limit(1)
    #         )

    #         result = await session.execute(stmt)
    #         result = result.scalar_one_or_none()
            
    #         return result

    @staticmethod
    async def get_user_by_creds(user_creds: str) -> UsersBase | None:
        async with async_session() as session:
            text_fields = func.concat_ws(
                ' ',
                func.coalesce(UsersBase.first_name, ''),
                func.coalesce(UsersBase.last_name, ''),
                func.coalesce(UsersBase.username, ''),
                func.coalesce(UsersBase.job_title, '')
            )

            tsvector = func.to_tsvector('russian', text_fields).op('||')(
                func.to_tsvector('english', text_fields)
            )

            tsquery = func.websearch_to_tsquery('russian', user_creds).op('||')(
                func.websearch_to_tsquery('english', user_creds)
            )

            rank = func.ts_rank(tsvector, tsquery)

            stmt = (
                select(UsersBase, rank.label("rank"))
                .where(tsvector.op("@@")(tsquery))
                .order_by(desc(rank))
                .limit(1)
            )

            result = await session.execute(stmt)
            row = result.first()

            if row:
                user, _ = row
                return user
            return None

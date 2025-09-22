from sqlalchemy import select
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from models.models import UsersBase, UsersCallsAssociation
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from utils.useful.sql_sessions import (
    get_db,
    async_session
)

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

            user_again = await session.refresh(new_user)
            
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

from sqlalchemy import select
from schemas.user_pydantic_schemas.user_schema import UserTemplate
from models.models import UserBase
from sqlalchemy import select
from utils.useful.sql_sessions import (
    get_db,
    async_session
)

class AsyncRequestsUser:

    @staticmethod
    async def get_user_by_id(
        id: int
    ) -> UserBase:
        async with async_session() as session:
            stmt = (
                select(
                    UserBase
                )
                .where(
                    UserBase.id == id
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
    ) -> UserBase | None:
        async with async_session() as session:
            new_user = UserBase(
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
    ) -> list[UserBase]:
        async with async_session() as session:
            stmt = (
                select(
                    UserBase
                )
                .limit(page_size)
                .offset(page_offset * page_size)
                .order_by(
                    UserBase.id
                )
            )

            users = await session.execute(stmt)
            users = users.scalars().all()

            return users

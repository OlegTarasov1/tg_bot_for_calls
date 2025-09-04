from sqlalchemy import select
from aiogram import types
from models.models import Employee
from sqlalchemy import select
from utils.useful.sql_sessions import get_db

class AsyncRequestsUser:

    @staticmethod
    async def get_user_by_id(
        id: int
    ) -> Employee:
        async with get_db as session:
            stmt = (
                select(
                    Employee
                )
                .where(
                    Employee.id == id
                )
            )

            user = await session.execute(stmt)
            user = user.scalar_one_or_none()

            return user
            
            
    @staticmethod
    async def new_user(
        from_user: types.User
    ) -> Employee | None:
        async with get_db() as session:
            stmt = (
                select(
                    Employee
                )
                .where(
                    Employee.id == from_user.id
                )
            )

            user = await session.execute(stmt) 
            user = user.scalar_one_or_none()
            
            if user:
                return user
            
            new_user = Employee(
                **from_user.model_dump()
            )
            await session.add(new_user)

            user = await session.refresh(user)
            
            return user
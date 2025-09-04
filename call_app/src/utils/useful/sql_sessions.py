# from aiogram.utils.context import get_context
from config.database_config import EnvData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from collections.abc import AsyncGenerator


db_url = EnvData().url.render_as_string(hide_password = False)

async_engine = create_async_engine(db_url)
async_session = async_sessionmaker(async_engine)

# AsyncGenerator[AsyncSession]
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

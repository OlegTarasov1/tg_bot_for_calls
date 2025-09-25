from config.database_config import async_session
from db_manip.raw_data.calls import initial_calls 
from models.models import CallsBase
from sqlalchemy.dialects.postgresql import insert
import logging
import asyncio

async def init_basic_calls():
    async with async_session() as session:
        stmt = (
            insert(
                CallsBase
            )
            .values(
                initial_calls
            )
        )
        stmt = stmt.on_conflict_do_nothing(index_elements=['id'])

        await session.execute(stmt)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(
        init_basic_calls()
    )
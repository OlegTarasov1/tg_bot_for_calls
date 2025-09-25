from views.routers import routers
import asyncio
import os
from aiogram import (
    Bot,
    Dispatcher
)


async def main():
    bot = Bot(token = os.getenv("BOT_TOKEN"))

    dp = Dispatcher()
    dp.include_router(routers)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
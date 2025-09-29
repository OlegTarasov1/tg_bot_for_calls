from middleware.inner_middleware.authorization_middleware import AuthorizationMiddleware
from views.admin_pannel.pannel_handler import admin_pannel_router
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
    dp.message.outer_middleware(AuthorizationMiddleware())
    dp.include_router(routers)
    dp.include_router(admin_pannel_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())